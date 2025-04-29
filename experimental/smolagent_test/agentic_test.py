from typing import Optional
import os, toml

#from openai import OpenAI
from smolagents import HfApiModel, LiteLLMModel, TransformersModel, tool
from smolagents.agents import CodeAgent, ToolCallingAgent


#Short config
with open("../MRA_V1/.streamlit/secrets.toml", "r") as file:
    conf = toml.load(file)
os.environ["OPENAI_API_KEY"] = conf['general']['OPENAI_API_KEY']
model = LiteLLMModel(model_id="gpt-4o")



#Defining the tools
@tool
def get_training_list() -> list:
    """
    Obtenir la liste de tous les programmes d'apprentissage disponibles.

    Returns:
        Une liste de dictionnaires contenant les détails des programmes disponibles.
    """
    return [
        {"id": "1", "subject": "Python pour débutants", "field": "Programmation", "description": "Apprenez les bases de Python.","chapters":[]},
        {"id": "2", "subject": "Marketing digital", "field": "Marketing", "description": "Découvrez les bases du marketing digital.","chapters":[]},
        {"id": "3", "subject": "Gestion de projet agile", "field": "Management", "description": "Apprenez à gérer un projet de manière agile.","chapters":[]},
    ]


@tool
def get_all_training_summary_for_field(field: str) -> list:
    """
    Obtenir la liste des programmes d'apprentissage disponibles pour un domain particulier donné.

    Args:
        field: Le domaine pour lequel on veut obtenir les programmes parmi.

    Returns:
        Une liste de dictionnaires contenant les programmes du domaine spécifié.
    """
    all_trainings = {
        "Histoire": [
        {"id": "6", "subject": "Histoire médiévale", "description": "Explorez les événements clés du Moyen Âge.", "chapters": []},
        {"id": "7", "subject": "Révolutions et modernité", "description": "Comprenez les révolutions qui ont façonné le monde moderne.", "chapters": []},
    ],
    "Géographie": [
        {"id": "8", "subject": "Géographie physique", "description": "Analysez les caractéristiques naturelles de la Terre.", "chapters": []},
        {"id": "9", "subject": "Géopolitique contemporaine", "description": "Étudiez les relations internationales et les conflits actuels.", "chapters": []},
    ],
    "Économie": [
    ],
    "Sociologie": [
        {"id": "12", "subject": "Sociologie des organisations", "description": "Analysez le fonctionnement des organisations sociales.", "chapters": []},
        {"id": "13", "subject": "Sociologie de la famille", "description": "Étudiez l’évolution des structures familiales à travers l’histoire.", "chapters": []},
    ],
    "Science": [
        {"id": "14", "subject": "Physique fondamentale", "description": "Découvrez les lois fondamentales de la physique.", "chapters": []},
        {"id": "15", "subject": "Biologie cellulaire", "description": "Apprenez le fonctionnement des cellules et leur impact sur la vie.", "chapters": []},
    ],
    "Géologie": [
    ],
    }
    return all_trainings.get(field, [])


@tool
def create_training(subject: str, field: str, description : str) -> dict:
    """
    Créer un nouveau programme d'apprentissage à partir de la description fournie.

    Args:
        subject: Sujet du programme.
        field: Domaine du programme.
        description: Description du programme.

    Returns:
        Un dictionnaire contenant les détails du programme créé.
    """
    new_training = {
        "id": "99",
        "subject": subject,
        "field": field,
        "description": description,
    }
    return new_training


@tool
def subscribe_user_to_training(subject: str, phone: str, program_id: str) -> dict:
    """
    Souscrire un utilisateur à un programme d'apprentissage.

    Args:
        subject: Le prénom de l'utilisateur.
        phone: Le numéro de téléphone de l'utilisateur.
        program_id: L'identifiant du programme.

    Returns:
        Un dictionnaire confirmant l'inscription.
    """
    return {
        "user": subject,
        "phone": phone,
        "program_id": program_id,
        "status": "Inscription réussie",
    }




#Creating and calling the agent
agent = ToolCallingAgent(tools=[get_training_list,get_all_training_summary_for_field,create_training,subscribe_user_to_training], model=model)

request = ["J'aimerais me former encore davantage en Sociologie et j'ai déjà suivi les cours ici présents. Peux tu créer un cours qui n'existe pas déjà ?"
    
    "Quels sont les programmes disponibles en science et technologie, et pouvez-vous m'inscrire à l'un d'eux ?",  
    # 1-> get_all_training_summary_for_field("Science") + subscribe_user_to_training(nom, téléphone, program_id)

    "J'aimerais en savoir plus sur les formations en économie et en sociologie. Pouvez-vous me donner les programmes disponibles ?",  
    # 2-> get_all_training_summary_for_field("Économie") + get_all_training_summary_for_field("Sociologie")

    "Je veux créer un programme sur la cybersécurité dans le domaine de l'informatique et m'y inscrire immédiatement. Pouvez-vous le faire ?",  
    # 3-> create_training("Cybersécurité", "Informatique") + subscribe_user_to_training(nom, téléphone, program_id)

    "Quels sont tous les programmes disponibles ? J'aimerais m'inscrire à un en histoire.",  
    # 4-> get_training_list() + subscribe_user_to_training(nom, téléphone, program_id)

    "Pouvez-vous me lister les formations en histoire et géographie et créer une nouvelle formation sur l'archéologie ?",  
    # 5-> get_all_training_summary_for_field("Histoire") + get_all_training_summary_for_field("Géographie") + create_training("Archéologie", "Histoire")
]




print("ToolCallingAgent:", agent.run(request[1]))

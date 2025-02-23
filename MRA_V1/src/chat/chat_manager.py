import json
from openai import OpenAI
from backend.training_manager import TrainingManager
from backend.user_manager import UserManager
from backend.training_creator import TrainingCreator
import re
from chat.openai_agent import OpenAIAgent
import os

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_training_list",
            "description": "Obtenir la liste des programmes d'apprentissage disponibles",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_all_training_summary_for_field",
            "description": "Obtenir la liste des programmes d'apprentissage disponibles pour un domaine donné",
            "parameters": {
                "type": "object",
                "properties": {
                    "field": {
                        "type": "string",
                        "description": "le domaine pour lequel on veut obtenir les programmes d'apprentissage",
                    }
                },
                "required": ["field"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "create_training",
            "description": "Créer un nouveau programme d'apprentissage à partir de la description fournie",
            "parameters": {
                "type": "object",
                "properties": {
                    "subject": {
                        "type": "string",
                        "description": "Sujet du programme d'apprentissage",
                    },
                    "field": {
                        "type": "string",
                        "description": "Domaine du programme d'apprentissage",
                    },
                },
                "required": ["description", "field"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "subscribe_user_to_training",
            "description": "Souscrire un utilisateur à un programme d'apprentissage",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Le prenom de l'utilisateur",
                    },
                    "phone": {
                        "type": "string",
                        "description": "Le numéro de téléphone de l'utilisateur",
                    },
                    "program_id": {
                        "type": "string",
                        "description": "L'identifiant du programme d'apprentissage",
                    },
                },
                "required": ["description"],
            },
        },
    },
]


class ChatManager:
    def __init__(self):
        self.openai_agent = OpenAIAgent()
        self.messages = []
        print("Current Working Directory:", os.getcwd())
        with open("src/chat/select_prompt.txt", "r") as file:
            self.messages.append(
                {"role": "system", "content": file.read(), "display": False}
            )
        self.training_manager = TrainingManager()
        self.user_manager = UserManager()
        self.training_creator = TrainingCreator()
        self.session_finished = False

    def get_next_message(self):
        dialog_finished = False
        assistant_message = None
        while not dialog_finished:
            response = self.openai_agent.generate_response(
                messages=self.messages, tools=tools
            )
            assistant_message = response.choices[0].message
            print(f"assistant_message: {assistant_message}")

            if assistant_message.tool_calls:
                print("assistant_message.tool_calls: ",
                      assistant_message.tool_calls)
                tool_call = assistant_message.tool_calls[0]
                function_name = tool_call.function.name
                arguments = json.loads(tool_call.function.arguments)
                self.messages.append(assistant_message)
                print(
                    f"call Function name: {function_name} with arguments: {arguments}"
                )

                if function_name == "get_training_list":
                    all_trainings = self.training_manager.get_all_training_summaries()
                    if all_trainings and len(all_trainings) > 0:
                        result = json.dumps(all_trainings)
                    else:
                        result = "Pas de programme d'apprentissage disponible"
                elif function_name == "get_all_training_summary_for_field":
                    all_trainings = self.training_manager.get_all_training_summary_for_field(
                        arguments["field"]
                    )
                    if all_trainings and len(all_trainings) > 0:
                        # convert the list of training to string by appending a new line with training name
                        result = "Trainings\n"
                        for training in all_trainings:
                            result += f"- {training.field} - {training.name} (training_id: {training.id})\n"
                    else:
                        result = "Pas de programme d'apprentissage disponible pour ce domaine"
                elif function_name == "create_training":
                    print(
                        "...Création d'un programme d'apprentissage avec : ",
                        arguments["subject"],
                    )
                    training = self.training_creator.create_and_add_to_db(
                        arguments["field"], arguments["subject"]
                    )
                    result = json.dumps(
                        f"training created {training.field} - {training.name}")
                elif function_name == "get_training_by_id":
                    training = self.training_manager.get_training_by_id(
                        arguments["id"])
                    if training:
                        result = f"{training.field} - {training.name} (training_id: {training.id})"
                    else:
                        result = "Aucun programme d'apprentissage trouvé"

                elif function_name == "subscribe_user_to_training":
                    user = self.user_manager.get_user_by_name(
                        arguments["name"])
                    user = self.user_manager.get_user_by_name(
                        arguments["name"])
                    if not user:
                        print(
                            f"...Creating user {arguments['name']} with phone {arguments['phone']}"
                        )
                        user = self.user_manager.create_user(
                            arguments["name"], arguments["phone"]
                        )
                    print(
                        f"...Subscribe user.id {user.id} to training  {arguments['program_id']}"
                    )
                    training = self.training_manager.get_training_by_id(
                        arguments["program_id"])
                    if training:
                        self.user_manager.start_training(
                            user, training)
                    result = "Utilisateur inscrit avec succès!"

                else:
                    print("Function not found")
                    result = "Function not found"
                # Add the function response back to the conversation
                print(f"---> result: {result}")
                self.messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": assistant_message.tool_calls[0].id,
                        "content": result,
                    }
                )
            else:
                dialog_finished = True
                # if the message content contains "```json", extract it
                if assistant_message.content and "```json" in assistant_message.content:
                    json_match = re.search(
                        r"```json(.*?)```", assistant_message.content, re.DOTALL
                    )
                    if json_match:
                        json_content = json_match.group(1).strip()
                        message_dict = json.loads(json_content)
                        text_before_json = assistant_message.content.split("```json")[
                            0
                        ].strip()
                        self.messages.append(
                            {
                                "role": assistant_message.role,
                                "content": text_before_json,
                                "json": message_dict,
                                "display": True,
                            }
                        )
                        self.session_finished = True
                else:
                    self.messages.append(
                        {
                            "role": assistant_message.role,
                            "content": assistant_message.content,
                            "display": True,
                        }
                    )

        return assistant_message

    def is_session_finished(self):
        return self.session_finished

    def respond_to_user(self, user_message):
        self.messages.append(
            {"role": "user", "content": user_message, "display": True})
        self.messages.append(
            {"role": "user", "content": user_message, "display": True})
        return self.get_next_message()

    def get_messages(self):
        return self.messages

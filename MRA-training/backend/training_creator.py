import json
from openai import OpenAI
from backend.catalog_manager import *
import toml




class TrainingCreator():
    def __init__(self):
        # load key from file ".streamlit/secrets.toml"
        with open(".streamlit/secrets.toml", "r") as file:
            conf = toml.load(file)
        self.client = OpenAI(api_key=conf['general']['OPENAI_API_KEY'])
        self.catalog_manager = TrainingManager()
    
    def create_training_json(self,field:str,subject:str) -> str:
        
        messages=[]
        
        with open("data/new_training_json_prompt.txt", "r") as file:
            file.replace("[[DOMAINE]]",field)
            file.replace("[[SUJET]]",subject)
            messages.append( {"role": "user", "content": file.read()})
        
        response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
            )
        
        self.training_json = json.loads(response.choices[0].message.content)
        
        print("first json chapter created :",self.training_json)
    
    
    
    def complete_chapters(self,field:str):
        chapters = []
        
        for chapter in self.training_json["chapters"]:
            messages=[]
            with open("data/new_chapter_json_prompt.txt", "r") as file:
                file.replace("[[DOMAINE]]",field)
                file.replace("[[SUJET]]",chapter["title"])
                messages.append( {"role": "user", "content": file.read()})
            
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
            )
            
            chapter["content"] = json.loads(response.choices[0].message.content)["content"]
            chapters.append(chapter)
            
        return chapters


        
    def create_and_add_to_db(self,field:str,subject:str):
        self.create_training_json(field,subject) #creates json in self.training_json
        
        
        chapters = self.complete_chapters(field)
        chapter_names = [chapter["title"] for chapter in chapters]
            
        print("training created, chapters :",chapter_names)
        print("saving to db")
        #self.TrainingManager.create_training(subject, field, 'a chapter about '+subject, chapter_names)

training_creator = TrainingCreator()
training_creator.create_and_add_to_db("Géologie","La fosse des Marianes")


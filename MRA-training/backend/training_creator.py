import json
import re
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
            content = file.read()
        content=content.replace("[[DOMAINE]]",field)
        content=content.replace("[[SUJET]]",subject)
        messages.append( {"role": "user", "content": content})
        
        response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
            )
        
        #on filtre ce qui'il y a entre les deux balises ```json et ``` dans response.choices[0].message.content
        json_content = re.search(r"```json(.*?)```", response.choices[0].message.content, re.DOTALL).group(1).strip()
        self.training_json = json.loads(json_content)
        
        print("first json chapter created : len = ",len(self.training_json),'-------------')
    
    
    
    def complete_chapters(self,field:str):
        chapters = []
        
        #Erreur ICI
        for chapter in self.training_json:
            messages=[]
            
            with open("data/complete_training_json_prompt.txt", "r") as file:
                content = file.read()
            content=content.replace("[[DOMAINE]]",field)
            content=content.replace("[[NOM_CHAPITRE]]",chapter["name"])
            messages.append( {"role": "user", "content": content})
            
            response_complete = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
            )
            
            json_content_complete = re.search(r"```json(.*?)```", response_complete.choices[0].message.content, re.DOTALL).group(1).strip()
            json_content_complete = json_content_complete.replace("\n","")
            #list indices must be integers or slices, not str ??????????
            chapter["content"] = json.loads(json_content_complete)["content"]
            chapter["question"] = json.loads(json_content_complete)["question"]
            chapter["reponses"] = json.loads(json_content_complete)["responses"]
            chapters.append(chapter)
            print("chapter completed : ",chapter["name"])
            
        return chapters


        
    def create_and_add_to_db(self,field:str,subject:str):
        self.create_training_json(field,subject) #creates json in self.training_json
        
        
        chapters = self.complete_chapters(field)
        chapter_names = [chapter["name"] for chapter in chapters]
            
        print('training created, saving ',len(chapters),' chapters to db')

        return self.catalog_manager.create_training(subject, field, 'Un training sur '+subject, chapters)


import json, re, toml, threading, itertools
from backend.catalog_manager import Training, TrainingManager
from concurrent.futures import ThreadPoolExecutor
from backend.openai_agent import OpenAIAgent
from typing import List, Dict
from prisma import Prisma


class TrainingCreator:
    def __init__(self):
        self.openai_agent = OpenAIAgent()
        self.catalog_manager = TrainingManager()
        self.db = Prisma()
        self.db.connect()

        # intialize a first training if the database is empty
        print('checking if database is empty')
        a_training  =self.db.training.find_first()
        if not a_training:
            print('database is empty, creating first training')
            self.create_and_add_to_db("Médecine", "Tendinite rotulienne")
    
    def create_training_json(self, field: str, subject: str) -> str:
        messages = []
        with open("data/new_training_json_prompt.txt", "r") as file:
            content = file.read()
        content = content.replace("[[DOMAINE]]", field)
        content = content.replace("[[SUJET]]", subject)
        messages.append({"role": "user", "content": content})
        
        response = self.openai_agent.generate_response( messages=messages)
        return self.openai_agent.extract_json_content(response)
    
    def complete_chapter(self, chapter, field, training_id, subject, transaction: PrismaTransaction):
        messages = []
        with open("data/complete_training_json_prompt.txt", "r") as file:
            content = file.read()
        content = content.replace("[[DOMAINE]]", field)
        content = content.replace("[[NOM_CHAPITRE]]", chapter["name"])
        content = content.replace("[[SUJET]]", subject)
        messages.append({"role": "user", "content": content})
        
        response_complete = self.openai_agent.generate_response( messages=messages)
        json_content_complete = self.openai_agent.extract_json_content(response_complete)

        return json_content_complete
        chapter["content"] = json.loads(json_content_complete)["content"]
        chapter["question"] = json.loads(json_content_complete)["question"]
        chapter["reponses"] = json.loads(json_content_complete)["responses"]
        chapter["training_id"] = training_id

        answers_json = json_content_complete["responses"]

        self.transaction.chapter.create(
            data={
                'name': name,
                'content': content,
                'question': question,
                'answers': json_content_complete["responses"],
                'training_id': training_id,
            }
        )

        return self.db.chapter.create(
            data={
                'name': name,
                'content': content,
                'question': question,
                'answers': answers_json,
                'training_id': training_id,
            }
        )

        
        catalog_manager.add_chapter_to_training(chapter["name"], chapter["content"], chapter["question"], chapter["reponses"], chapter["training_id"])
        transaction: 
        print('chapter added to database : ', chapter["name"])
    

    def create_chapter(self, field: str, subject: str, training: Training, chapter_id: int, chapter_name: str)
        messages = []
        with open("data/complete_training_json_prompt.txt", "r") as file:
            content = file.read()
        content = content.replace("[[DOMAINE]]", field)
        content = content.replace("[[NOM_CHAPITRE]]", chapter["name"])
        content = content.replace("[[SUJET]]", subject)
        messages.append({"role": "user", "content": content})
        
        response_complete = self.openai_agent.generate_response( messages=messages)
        json_content_complete = self.openai_agent.extract_json_content(response_complete)

        self.db.chapter.create(
            data={
                'id': chapter_id,
                'name': chapter_name,
                'content': json_content_complete["content"],
                'question': json_content_complete["question"],
                'answers': json_content_complete["responses"],
                'training': training,
            }
        )
        

    def create_and_add_to_db(self, field: str, subject: str):
        print('Creating training...')
        training_json : List[Dict[str, str]] = self.create_training_json(field, subject)
        training: Training = self.db.training.create(
          data={
              'name': subject,
              'field': field,
              'description': "Training sur "+subject,
          }
        )
        print('Creating chapters...')
        with ThreadPoolExecutor() as executor:
            for chapter in training_json:
                executor.submit(self.create_chapter, field, subject, training, chapter["id"], chapter["name"])

def main():
    training_creator = TrainingCreator()
    training_creator.create_and_add_to_db("Médecine", "Tendinite rotulienne")

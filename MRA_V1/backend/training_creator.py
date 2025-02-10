import json, re, toml, threading, itertools
from backend.catalog_manager import TrainingManager
from concurrent.futures import ThreadPoolExecutor
from backend.openai_agent import OpenAIAgent

class TrainingCreator:
    def __init__(self):
        self.openai_agent = OpenAIAgent()
        self.catalog_manager = TrainingManager()
    
    async def create_training_json(self, field: str, subject: str) -> str:
        messages = []
        with open("data/new_training_json_prompt.txt", "r") as file:
            content = file.read()
        content = content.replace("[[DOMAINE]]", field)
        content = content.replace("[[SUJET]]", subject)
        messages.append({"role": "user", "content": content})
        
        response = self.openai_agent.create_completion(model="gpt-4o-mini", messages=messages)
        return self.openai_agent.extract_json_content(response)
    
    async def complete_chapter(self, chapter, field, training_id, subject):
        messages = []
        with open("data/complete_training_json_prompt.txt", "r") as file:
            content = file.read()
        content = content.replace("[[DOMAINE]]", field)
        content = content.replace("[[NOM_CHAPITRE]]", chapter["name"])
        content = content.replace("[[SUJET]]", subject)
        messages.append({"role": "user", "content": content})
        
        response_complete = self.openai_agent.create_completion(model="gpt-4o-mini", messages=messages)
        json_content_complete = self.openai_agent.extract_json_content(response_complete)

        chapter["content"] = json.loads(json_content_complete)["content"]
        chapter["question"] = json.loads(json_content_complete)["question"]
        chapter["reponses"] = json.loads(json_content_complete)["responses"]
        chapter["training_id"] = training_id

        await self.catalog_manager.add_chapter_to_training(chapter["name"], chapter["content"], chapter["question"], chapter["reponses"], chapter["training_id"])
        print('chapter added to database : ', chapter["name"])
    
    async def execute_in_parallel(self, subject, field, training, training_json):
        with ThreadPoolExecutor() as executor:
            print('subject : ', subject, 'field : ', field, 'training : ', training)
            list(executor.map(self.complete_chapter, training_json, itertools.repeat(field), itertools.repeat(training.id), itertools.repeat(subject)))
            print('done with all chapters')
    
    async def create_and_add_to_db(self, field: str, subject: str):
        training = await self.catalog_manager.create_training(subject, field, 'Un training sur ' + subject)
        print("Training created and saved to database ")

        training_json = await self.create_training_json(field, subject)

        await self.execute_in_parallel(subject, field, training, training_json)
        print('Training complete')

async def main():
    training_creator = TrainingCreator()
    await training_creator.create_and_add_to_db("Médecine", "Tendinite rotulienne")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
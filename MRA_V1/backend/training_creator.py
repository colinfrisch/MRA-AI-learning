import json, re, toml, threading
from openai import OpenAI
from backend.catalog_manager import *
from concurrent.futures import ThreadPoolExecutor



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
        
        
    
    
    
    def complete_chapter(self,chapter,field):
        
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
        #print ("-----------------")
        #print (response_complete.choices[0].message.content)
        
        json_content_complete = re.search(r"```json(.*?)```", response_complete.choices[0].message.content, re.DOTALL).group(1).strip()
        json_content_complete = json_content_complete.replace("\n","")
        

        chapter["content"] = json.loads(json_content_complete)["content"]
        chapter["question"] = json.loads(json_content_complete)["question"]
        chapter["reponses"] = json.loads(json_content_complete)["responses"]

        print("chapter completed : ",chapter["name"],' -------------')
            
        return chapter
    
    def execute_in_parallel(self,chapters,field,subject,training:Training):
        with ThreadPoolExecutor() as executor:
            results = list(executor.map(self.complete_chapter, self.training_json, field))
            chapters.extend(results)
            print('done with all chapters')
            #return self.catalog_manager.create_training(subject, field, 'Un training sur ' + subject, chapters)
            return self.catalog_manager.modify_chapters(training.id, chapters)



        
    def create_and_add_to_db(self,field:str,subject:str):
        training = self.catalog_manager.create_training(subject, field, 'Un training sur ' + subject, []) #Training(db.cursor.lastrowid, name, field, description, chapters)
        print("Training created and saved to database : len = ",'-------------')

        #/!\ remplacer les self.training_json par training_json (paramètres plutot que variables d'instance)
        self.create_training_json(field,subject) #creates json in self.training_json

        
        chapters = []
        
        thread = threading.Thread(target=self.execute_in_parallel, args=(chapters,field,subject,training))
        thread.start()
        
        print('training is being created ... saving ',len(chapters),' chapters to db -------------------------------------')

        



def main():
    training_creator = TrainingCreator()
    training_creator.create_and_add_to_db("Géographie","Singapour")
if __name__ == "__main__":
    main()

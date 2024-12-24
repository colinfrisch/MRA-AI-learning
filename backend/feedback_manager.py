#Objectif général : modifier le json 'chapitres' en fonction des retours des clients

import json
from openai import OpenAI
import streamlit as st
import catalog_manager
import toml



functions = [
  {
          "name": "get_chapter_content",
          "description": "Obtenir le contenu d'un chapitre du programme d'apprentissage.",
          "parameters": {
              "type": "object",
              "properties": {
                  "chapter_name": {
                      "type": "string",
                      "description": "Le nom du chapitre"
                  }
              },
              "required": ["chapter_name"],
          }
      },
  {
     
          "name": "get_chapter_list",
          "description": "Obtenir la liste des chapitres du programme d'apprentissage et leur description",
          "parameters": {
              "type": "object",
              "properties": {},
              "required": [],
          }
      }
]



class FeedbackManager():
    def __init__(self):
        # load key from file "../.streamlit/secrets.toml"
        with open("../.streamlit/secrets.toml", "r") as file:
            conf = toml.load(file)
        self.client = OpenAI(api_key=conf['general']['OPENAI_API_KEY'])

    def process_feedback(self,feedback_content:str) -> str : #Renvoie la liste des modifications effectuées (str)
        # create a prompt to ask chatGPT to process the feedback
        messages=[]
        with open("../data/feedback_prompt.txt", "r") as file:
            messages.append( {"role": "user", "content": file.read()+feedback_content})
        

        #call chatGPT
        dialog_finished = False
        while not dialog_finished :
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                functions=functions,
                function_call="auto"
            )
            print("----message")
            print(response.choices[0].message)
            if "function_call" in response.choices[0].message:
                function_call = response.choices[0].message['function_call']
                function_name = function_call['name']
                arguments = function_call['arguments']
                result = ''
                
                if function_name == "get_chapter_content":
                    # Parse arguments and call the function
                    args = json.loads(arguments)
                    result = catalog_manager.get_chapter_content(args["chapter_name"])

                    # Add the function response back to the conversation
                    messages.append({
                        "role": "function",
                        "name": function_name,
                        "content": str(result)
                    })
                
                if function_name == "get_chapter_list":
                    # Parse arguments and call the function
                    result = catalog_manager.get_chapter_list()

                # Add the function response back to the conversation
                messages.append({
                    "role": "function",
                    "name": function_name,
                    "content": str(result)
                })
                
            else :
                dialog_finished = True 
        return messages[-1]["content"]



def main():
    feedback = FeedbackManager().process_feedback("je voudrais en savoit plus sur les api")
    print(feedback)
    

main()
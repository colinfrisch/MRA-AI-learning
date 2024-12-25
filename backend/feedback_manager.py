#Objectif général : modifier le json 'chapitres' en fonction des retours des clients

import json
from openai import OpenAI
import streamlit as st
from catalog_manager import CatalogManager
import toml


tools = [
  { "type": "function",
     "function":{
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
      }
  },
  {"type": "function",
     "function":{
          "name": "get_chapter_list",
          "description": "Obtenir la liste des chapitres du programme d'apprentissage et leur description",
          "parameters": {
              "type": "object",
              "properties": {},
              "required": [],
          }
      }
  }
]



class FeedbackManager():
    def __init__(self):
        # load key from file ".streamlit/secrets.toml"
        with open(".streamlit/secrets.toml", "r") as file:
            conf = toml.load(file)
        self.client = OpenAI(api_key=conf['general']['OPENAI_API_KEY'])
        self.catalog_manager = CatalogManager()

    def process_feedback(self,feedback_content:str) -> str : #Renvoie la liste des modifications effectuées (str)
        # create a prompt to ask chatGPT to process the feedback
        messages=[]
        with open("data/feedback_prompt.txt", "r") as file:
            messages.append( {"role": "user", "content": file.read()+feedback_content})
        

        #call chatGPT
        dialog_finished = False
        while not dialog_finished :
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                tools=tools,
            )
            messages.append(response.choices[0].message)
            if response.choices[0].message.tool_calls:
                tool_call = response.choices[0].message.tool_calls[0]
                function_name = tool_call.function.name
                arguments = json.loads(tool_call.function.arguments)
                
                if function_name == "get_chapter_content":
                    # Parse arguments and call the function
                    result = self.catalog_manager.get_chapter_content(arguments["chapter_name"])

                if function_name == "get_chapter_list":
                    # Parse arguments and call the function
                    result = "\n".join(self.catalog_manager.get_chapter_list())


                # Add the function response back to the conversation
                messages.append({
                    "role": "tool",
                    "tool_call_id": response.choices[0].message.tool_calls[0].id,
                    "content":  result
                })
                
            else :
                dialog_finished = True 
        return messages[-1]["content"]



def main():
    feedback = FeedbackManager().process_feedback("je voudrais en savoit plus sur les api")
    print(feedback)
    

main()
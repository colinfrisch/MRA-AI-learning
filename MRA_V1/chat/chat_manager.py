import json
from openai import OpenAI
from backend.catalog_manager import TrainingManager
from backend.user_manager import UserManager
from backend.training_creator import TrainingCreator
import toml
import re


tools = [
  { "type": "function",
     "function":{
          "name": "get_training_list",
          "description": "Obtenir la liste des programmes d'apprentissage disponibles",
          "parameters": {
              "type": "object",
              "properties": {},
              "required": [],
          }
      }
  },
    {"type": "function",
     "function":{
          "name": "get_all_training_summary_for_field",
          "description": "Obtenir la liste des programmes d'apprentissage disponibles pour un domaine donné",
           "parameters": {
              "type": "object",
              "properties": {
                  "field": {
                      "type": "string",
                      "description": "le domaine pour lequel on veut obtenir les programmes d'apprentissage"
                  }
              },
              "required": ["field"],
          }
      }
  },
    {"type": "function",
     "function":{
          "name": "create_training",
          "description": "Créer un nouveau programme d'apprentissage à partir de la description fournie",
           "parameters": {
              "type": "object",
              "properties": {
                  "subject": {
                      "type": "string",
                      "description": "Sujet du programme d'apprentissage"
                  },
                  "field": {
                      "type": "string",
                      "description": "Domaine du programme d'apprentissage"
                  }
              },
              "required": ["description", "field"],
          }
      }
  },
    {"type": "function",
     "function":{
          "name": "subscribe_user_to_training",
          "description": "Souscrire un utilisateur à un programme d'apprentissage",
           "parameters": {
              "type": "object",
              "properties": {
                  "name": {
                      "type": "string",
                      "description": "Le prenom de l'utilisateur"
                  },
                   "phone": {
                      "type": "string",
                      "description": "Le numéro de téléphone de l'utilisateur"
                  },
                   "program_id": {
                      "type": "string",
                      "description": "L'identifiant du programme d'apprentissage"
                  },
              },
              "required": ["description"],
          }
      }
  }
]

class ChatManager:
  def __init__(self):
      # load key from file ".streamlit/secrets.toml"
      with open(".streamlit/secrets.toml", "r") as file:
          conf = toml.load(file)
      self.client = OpenAI(api_key=conf['general']['OPENAI_API_KEY'])
      self.messages = []
      with open("chat/select_prompt.txt", "r") as file:
          self.messages.append( {"role": "system", "content": file.read(), "display": False})
      self.training_manager = TrainingManager()
      self.user_manager = UserManager()
      self.training_creator = TrainingCreator()
      self.session_finished = False

  def get_next_message(self):
      dialog_finished = False
      while not dialog_finished:
          response = self.client.chat.completions.create(
              model="gpt-4o-mini",
              messages=self.messages,
              tools=tools,
          )
          assistant_message = response.choices[0].message
          if assistant_message.tool_calls:
              tool_call = assistant_message.tool_calls[0]
              function_name = tool_call.function.name
              arguments = json.loads(tool_call.function.arguments)
              self.messages.append(assistant_message)
              print(f"call Function name: {function_name} with arguments: {arguments}")

              if function_name == "get_training_list":
                  result = json.dumps(self.training_manager.get_all_training_summaries())

              elif function_name == "get_all_training_summary_for_field":
                  result = json.dumps(self.training_manager.get_all_training_summary_for_field(arguments["field"]))

              elif function_name == "create_training":
                  print("...Création d'un programme d'apprentissage avec : ", arguments["subject"])
                  training = self.training_creator.create_and_add_to_db(arguments["field"], arguments["subject"])
                  result = json.dumps(training.to_dict())

              elif function_name == "subscribe_user_to_training":
                  user = self.user_manager.get_user_by_name(arguments["name"])
                  if not user:
                      print(f"...Creating user {arguments['name']} with phone {arguments['phone']}")
                      user = self.user_manager.create_user(arguments["name"], arguments["phone"])
                  print(f"...Subscribe user.id {user.id} to training  {arguments['program_id']}")
                  self.user_manager.set_current_training(user.id, arguments["program_id"])
                  result = "Utilisateur inscrit avec succès!"
                  
              else:
                  print("Function not found")
                  result = "Function not found"
              # Add the function response back to the conversation
              self.messages.append({
                  "role": "tool",
                  "tool_call_id": response.choices[0].message.tool_calls[0].id,
                  "content":  result,
              })
          else:
              dialog_finished = True
              # if the message content contains "```json", extract it
              if "```json" in assistant_message.content:
                  json_match = re.search(r"```json(.*?)```", assistant_message.content, re.DOTALL)
                  if json_match:
                      json_content = json_match.group(1).strip()
                      message_dict = json.loads(json_content)
                      text_before_json = assistant_message.content.split("```json")[0].strip()
                      self.messages.append({
                          "role": assistant_message.role,
                          "content": text_before_json,
                          "json": message_dict,
                           "display": True
                      })
                      self.session_finished = True
              else:                  
                self.messages.append({
                    "role": assistant_message.role,
                    "content":  assistant_message.content,
                    "display": True
                })
      
      return assistant_message
  
  def is_session_finished(self):
      return self.session_finished

  def respond_to_user(self, user_message):
      self.messages.append({"role": "user", "content": user_message, "display": True})
      return self.get_next_message()

  def get_messages(self):
      return self.messages  

def main():
    chat_manager = ChatManager()
    
    user_message = "Bonjour, pouvez-vous m'aider avec le programme d'apprentissage?"
    response = chat_manager.respond_to_user(user_message)
    print(response.content)

if __name__ == "__main__":
    main()



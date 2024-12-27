import json
from openai import OpenAI
from backend.catalog_manager import TrainingManager
import toml

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
          "description": "Creer un nouveau programme d'apprentissage à partir de la description fournie",
           "parameters": {
              "type": "object",
              "properties": {
                  "description": {
                      "type": "string",
                      "description": "Description précise du programme d'apprentissage"
                  }
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
          self.messages.append( {"role": "user", "content": file.read(), "display": True})
      self.training_manager = TrainingManager()


  def get_next_message(self):
      dialog_finished = False
      while not dialog_finished :
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
                  # Parse arguments and call the function
                  result = self.training_manager.get_all_training_summaries()

              if function_name == "get_all_training_summary_for_field":
                  # Parse arguments and call the function
                  result = "\n".join(self.training_manager.get_all_training_summary_for_field(arguments["field"]))

              if function_name == "create_training":
                  # Parse arguments and call the function
                  print("Création d'un programme d'apprentissage................... avec cotenu: ", arguments["description"])
                  result = "programme d'apprentissage créé avec succès"


              # Add the function response back to the conversation
              self.messages.append({
                  "role": "tool",
                  "tool_call_id": response.choices[0].message.tool_calls[0].id,
                  "content":  result,
              })
              
          else :
              print(f"Réponse finale: {assistant_message.content}")
              self.messages.append({
                  "role": assistant_message.role,
                  "content":  assistant_message.content,
                  "display": True
              })
              dialog_finished = True 
      
      return assistant_message
  
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



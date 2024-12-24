#Objectif général : modifier le json 'chapitres' en fonction des retours des clients

from pydantic import BaseModel
import openai
from openai import OpenAI

client = OpenAI()



tools = [
  {
      "type": "function",
      "function": {
          "name": "get_chapter_content",
          "description": "Obtenir le contenu d'un chapitre du programme d'apprentissage. Appelle-le dès qu'un utilisateur fait un retour sur un chapitre précis. Par exemple, lorsqu'un utilisateur dit 'Outils de résumé : le chapitre n'était pas assez développé'",
          "parameters": {
              "type": "object",
              "properties": {
                  "order_id": {
                      "type": "string",
                      "description": "Le contenu du chapitre"
                  }
              },
              "required": ["order_id"],
              "additionalProperties": False
          }
      }
  }
]

def get_chapter(user_prompt):
    messages = []
    messages.append({"role": "system", "content": "Tu es un employé de service après vente utile et agréable. Utilises les outils fournis pour aider l'utilisateur."})
    messages.append({"role": "user", "content": user_prompt})

    response = client.beta.chat.completions.create(
        model='gpt-4o-2024-08-06',
        messages=messages,
        tools=tools
    )

    return response.choices[0].message.tool_calls[0].function
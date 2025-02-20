import os
import re
import json
from openai import OpenAI
from openai.types.chat import ChatCompletion

json_pattern = re.compile(r"```json\s*(.*?)```", re.DOTALL)



class OpenAIAgent:
    def __init__(self, mock=False):
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")
        self.client = OpenAI(api_key=api_key)
        self.mock = mock

    def generate_response(self, messages: list[dict], tools: list[dict]= None) -> ChatCompletion:
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            tools=tools,
        )
        return response


    # create a training table of content
    def create_training_summary(self, field: str, subject: str) -> str:
        messages = []
        with open("./chat/new_training_json_prompt.txt", "r") as file:
            content = file.read()
        content = content.replace("[[DOMAINE]]", field)
        content = content.replace("[[SUJET]]", subject)
        messages.append({"role": "user", "content": content})
        
        if self.mock:
            response_content = TRAINING_SAMPLE
        else :
          response_content = self.openai_agent.generate_response( messages=messages).choice[0].message.content
        return self.extract_json_content(response_content)
  

    # create the content of a chapter
    def create_chapter_content(self, field, subject, chapter_name):
        messages = []
        with open("./chat/complete_training_json_prompt.txt", "r") as file:
            content = file.read()
        content = content.replace("[[DOMAINE]]", field)
        content = content.replace("[[NOM_CHAPITRE]]", chapter_name)
        content = content.replace("[[SUJET]]", subject)
        messages.append({"role": "user", "content": content})

        if self.mock:
          response_content = CHAPTERS_CONTENT          
        else:
          response_content = self.generate_response( messages=messages).choice[0].message.content
        return  self.extract_json_content(response_content)


    def extract_json_content(self, content: str) -> any:
        json_content = json_pattern.search(content).group(1).strip()
        try:
          return json.loads(json_content)
        except json.JSONDecodeError as je :
          print ("Cannot decode response: ", content)
          print(je)
          raise je

TRAINING_SAMPLE="""
blah blah
```json
[
{"id": "1","name": "Tendinite"},
{"id": "2","name": "Genou"},
{"id": "3","name": "Tendinite au genou"}
]
```
"""

CHAPTERS_CONTENT="""
blah
```json
{"content": "Blah Blah Blah","question": "Chat do you think of blah?","responses": [{"text": "Texte de la réponse 1", "valid": "true"},{"text": "Texte de la réponse 2", "valid": "false"},{"text": "Texte de la réponse 3", "valid": "false"},{"text": "Texte de la réponse 4", "valid": "false"},{"text": "Texte de la réponse 5", "valid": "false"}]}
```
"""
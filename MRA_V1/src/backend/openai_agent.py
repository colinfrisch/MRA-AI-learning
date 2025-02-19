import os
import re
import json
from openai import OpenAI
from openai.types.chat import ChatCompletion


class OpenAIAgent:
    def __init__(self):
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")
        self.client = OpenAI(api_key=api_key)

    def generate_response(self, messages: list[dict], tools: list[dict]= None) -> ChatCompletion:
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            tools=tools,
        )
        return response

    def extract_json_content(self, response: dict) -> any:
        json_content = re.search(r"```json(.*?)```", response.choices[0].message.content, re.DOTALL).group(1).strip()
        try:
          return json.loads(json_content)
        except json.JSONDecodeError as je :
          print (response.choices[0].message.content)
          print(json_content)
          print(je)
          raise je

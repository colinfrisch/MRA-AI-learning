import os
import re
import json
from openai import OpenAI

class OpenAIAgent:
    def __init__(self):
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")
        self.client = OpenAI(api_key=api_key)

    def create_completion(self, model: str, messages: list[dict]) -> dict:
        response = self.client.chat.completions.create(
            model=model,
            messages=messages,
        )
        return response

    def generate_response(self, messages: list[dict], tools: list[dict]) -> dict:
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            tools=tools,
        )
        return response

    def extract_json_content(self, response: dict) -> dict:
        json_content = re.search(r"```json(.*?)```", response.choices[0].message.content, re.DOTALL).group(1).strip()
        return json.loads(json_content)
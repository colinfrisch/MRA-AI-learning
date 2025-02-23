import os
import re
import json
from openai import OpenAI
from openai.types.chat import ChatCompletion

json_pattern = re.compile(r"```json\s*(.*?)```", re.DOTALL)


class OpenAIAgent:
    def __init__(self):
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")
        self.client = OpenAI(api_key=api_key)

    def generate_response(self, messages: list[dict], tools: list[dict] = None) -> ChatCompletion:
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            tools=tools,
        )
        return response

    # create a training table of content

    def create_training_summary(self, field: str, subject: str):
        messages = []
        with open("./chat/new_training_json_prompt.txt", "r") as file:
            content = file.read()
        content = content.replace("[[DOMAINE]]", field)
        content = content.replace("[[SUJET]]", subject)
        messages.append({"role": "user", "content": content})

        response_content = self.generate_response(
            messages=messages).choices[0].message.content
        return self.extract_json_content(response_content) if response_content else None

    # create the content of a chapter
    def create_chapter_content(self, field, subject, chapter_name):
        messages = []
        with open("./chat/complete_training_json_prompt.txt", "r") as file:
            content = file.read()
        content = content.replace("[[DOMAINE]]", field)
        content = content.replace("[[NOM_CHAPITRE]]", chapter_name)
        content = content.replace("[[SUJET]]", subject)
        messages.append({"role": "user", "content": content})

        response_content = self.generate_response(
            messages=messages).choices[0].message.content
        return self.extract_json_content(response_content) if response_content else None

    def extract_json_content(self, content: str):
        match = json_pattern.search(content)
        if not match:
            return None
        else:
            json_content = match.group(1).strip()
            try:
                return json.loads(json_content)
            except json.JSONDecodeError as je:
                print("Cannot decode response: ", content)
                print(je)
                raise je

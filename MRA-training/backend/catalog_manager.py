# training_manager.py
from backend.db import DBConnection
import json
from enum import Enum

class Domain(Enum):
    HISTORY = "HISTORY"
    ECONOMY = "ECONOMY"
    GEOGRAPHY = "GEOGRAPHY"

class Response:
    def __init__(self, text: str, valid: bool):
        self.text = text
        self.valid = valid

    def to_dict(self):
        return {"text": self.text, "valid": self.valid}

class Chapter:
    def __init__(self, chapter_id: int, content: str, question: str, responses: list[Response]):
        self.id = chapter_id
        self.content = content
        self.question = question
        self.responses = responses

    def get_responses(self) -> list[Response]:
        return self.responses

    def to_dict(self):
        return {
            "id": self.id,
            "content": self.content,
            "question": self.question,
            "responses": [response.to_dict() for response in self.responses]
        }

class Training:
    def __init__(self, training_id: int, name: str, domain: Domain, description: str, chapters: list[Chapter]):
        self.id = training_id
        self.name = name
        self.domain = domain
        self.description = description
        self.chapters = chapters

    def get_name(self) -> str:
        return self.name

    def get_domain(self) -> Domain:
        return self.domain

    def get_description(self) -> str:
        return self.description

    def get_chapters(self) -> list[Chapter]:
        return self.chapters

class TrainingManager:
    def create_training(self, name: str, domain: Domain, description: str, chapters: list[Chapter]):
        with DBConnection() as db:
            chapters_json = json.dumps([chapter.to_dict() for chapter in chapters])
            db.execute("INSERT INTO trainings (name, domain, description, chapters) VALUES (?, ?, ?, ?)", 
                       (name, domain.value, description, chapters_json))
            db.commit()

    def get_all_trainings(self) -> list[Training]:
        with DBConnection() as db:
            db.execute("SELECT * FROM trainings")
            rows = db.fetchall()
            trainings = []
            for row in rows:
                chapters_data = json.loads(row["chapters"])
                chapters = [Chapter(chapter["id"], chapter["content"], chapter["question"], 
                                    [Response(resp["text"], resp["valid"]) for resp in chapter["responses"]]) 
                            for chapter in chapters_data]
                training = Training(row["id"], row["name"], Domain(row["domain"]), row["description"], chapters)
                trainings.append(training)
            return trainings

def main():
    training_manager = TrainingManager()
    chapters = [
        Chapter(1, "Content 1", "Question 1", [Response("Answer 1", True), Response("Answer 2", False)]),
        Chapter(2, "Content 2", "Question 2", [Response("Answer 3", True), Response("Answer 4", False)])
    ]
    training_manager.create_training("Training 1", Domain.HISTORY, "Description 1", chapters)
    trainings = training_manager.get_all_trainings()
    for training in trainings:
        print("Training Name:", training.get_name())
        print("Domain:", training.get_domain().value)
        print("Description:", training.get_description())
        for chapter in training.get_chapters():
            print("Chapter ID:", chapter.id)
            print("Content:", chapter.content)
            print("Question:", chapter.question)
            for response in chapter.get_responses():
                print("Response:", response.text, "Valid:", response.valid)

if __name__ == "__main__":
    main()

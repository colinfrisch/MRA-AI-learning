# training_manager.py
from backend.db import DBConnection
import json
from enum import Enum


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
    def __init__(self, training_id: int, name: str, field: str, description: str, chapters: list[dict]):
        self.id = training_id
        self.name = name
        self.field = field
        self.description = description
        self.chapters = chapters

    def get_name(self) -> str:
        return self.name

    def get_field(self) -> str:
        return self.field

    def get_description(self) -> str:
        return self.description

    def get_chapters(self) -> list[dict]:
        return self.chapters

class TrainingManager:
    def create_training(self, name: str, field: str, description: str, chapters: list[dict]):
        with DBConnection() as db:
            chapters_json = json.dumps([chapter for chapter in chapters])
            db.execute("INSERT INTO trainings (name, field, description, chapters) VALUES (?, ?, ?, ?)", 
                       (name, field, description, chapters_json))
            db.commit()
        # return the training 
        return Training(db.cursor.lastrowid, name, field, description, chapters)

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
                training = Training(row["id"], row["name"], row["field"], row["description"], chapters)
                trainings.append(training)
            return trainings

    def get_all_training_summaries(self) -> list[dict]:
        with DBConnection() as db:
            db.execute("SELECT id, name, field, description FROM trainings")
            rows = db.fetchall()
            training_summaries = []
            for row in rows:
                training_summary = {
                    "id": row["id"],
                    "name": row["name"],
                    "field": row["field"],
                    "description": row["description"]
                }
                training_summaries.append(training_summary)
            return training_summaries

    def get_all_training_summary_for_field(self, field: str) -> list[dict]:
        all_summaries = self.get_all_training_summaries()
        return [summary for summary in all_summaries if summary["field"] == field]

def main():
    training_manager = TrainingManager()
    chapters = [
        Chapter(1, "Content 1", "Question 1", [Response("Answer 1", True), Response("Answer 2", False)]),
        Chapter(2, "Content 2", "Question 2", [Response("Answer 3", True), Response("Answer 4", False)])
    ]
    training_manager.create_training("Training 1", "history", "Description 1", chapters)
    trainings = training_manager.get_all_trainings()
    for training in trainings:
        print("Training Name:", training.get_name())
        print("Field:", training.get_field())
        print("Description:", training.get_description())
        for chapter in training.get_chapters():
            print("Chapter ID:", chapter.id)
            print("Content:", chapter.content)
            print("Question:", chapter.question)
            for response in chapter.get_responses():
                print("Response:", response.text, "Valid:", response.valid)

if __name__ == "__main__":
    main()

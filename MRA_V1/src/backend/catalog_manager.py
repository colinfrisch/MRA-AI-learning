# training_manager.py
from prisma import Prisma
import json
from typing import List, Optional
from prisma.models import Training, Chapter


class Answer:
    def __init__(self, text: str, valid: bool):
        self.text = text
        self.valid = valid

    def to_dict(self):
        return {"text": self.text, "valid": self.valid}



class TrainingManager:
    def __init__(self):
        self.db = Prisma()
        self.db.connect()

    def create_training(self, name: str, field: str, description: str) -> Training:
        return self.db.training.create(
            data={
                'name': name,
                'field': field,
                'description': description,
            }
        )

    def add_chapter_to_training(self, name: str, content: str, question: str, answers: list[dict], training_id: int) -> Chapter:
        answers_json = json.dumps(answers)
        return self.db.chapter.create(
            data={
                'name': name,
                'content': content,
                'question': question,
                'answers': answers_json,
                'training_id': training_id,
            }
        )

    def get_all_trainings(self) -> list[Training]:
        return self.db.training.find_many(include={'chapters': True})
       

    def get_all_training_summaries(self) -> list[Training]:
        return self.db.training.find_many(select={'id': True, 'name': True, 'field': True, 'description': True})

    def get_all_training_summary_for_field(self, field: str) -> list[Training]:
        all_summaries = self.get_all_training_summaries()
        return [summary for summary in all_summaries if summary["field"] == field]

    def get_training_by_id(self, training_id: int) -> Training:
        return self.db.training.find_unique(where={'id': training_id}, include={'chapters': True})

    def modify_chapter_section(self, chapter_id: int, section: str, new_content: str):
        self.db.chapter.update(
            where={'id': chapter_id},
            data={section: new_content}
        )

# training_manager.py
from prisma import Prisma
import json
from typing import List, Optional
from prisma.models import Training, Chapter


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

    def get_all_trainings(self) -> list[Training]:
        return self.db.training.find_many(include={'chapters': True})

    def get_all_training_summaries(self) -> list[Training]:
        return self.db.training.find_many(select={'id': True, 'name': True, 'field': True, 'description': True})

    def get_all_training_summary_for_field(self, field: str) -> list[Training]:
        return self.db.training.find_many(where={'field': field}, select={'id': True, 'name': True, 'field': True, 'description': True})

    def get_training_by_id(self, training_id: int) -> Training:
        return self.db.training.find_unique(where={'id': training_id}, include={'chapters': True})


#    def modify_chapter_section(self, chapter_id: int, section: str, new_content: str):
#        self.db.chapter.update(
#            where={'id': chapter_id},
#            data={section: new_content}
#        )

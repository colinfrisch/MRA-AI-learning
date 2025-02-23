
from backend.training_manager import TrainingManager
from concurrent.futures import ThreadPoolExecutor
from chat.openai_agent import OpenAIAgent
from typing import List, Dict
from prisma import Prisma, Json
from prisma.errors import PrismaError
from prisma.types import TrainingWhereInput
from prisma.models import Training, Chapter


class TrainingCreator:
    def __init__(self):
        self.openai_agent = OpenAIAgent()
        self.db = Prisma(log_queries=False)
        self.db.connect()

    # this methods checks that the training have chapters and create a fake training if none in tghe db
    def check_trainings(self):
        # remove trainings with no chapter
        # TODO: fix this
        # self.db.training.delete_many(
        #    where={'chapters':{''}}
        # )
        # intialize a first training if the database is empty
        print('checking if database is empty')
        a_training = self.db.training.find_first()
        if not a_training:
            print('database is empty, creating first training')
            self.create_and_add_to_db("Médecine", "Tendinite rotulienne")

    def create_chapter(self, field: str, subject: str, training: Training, chapter_number: int, chapter_name: str):
        json_content_complete = self.openai_agent.create_chapter_content(
            field, subject, chapter_name)
        print("Saving chapter ", chapter_name)
        print("Training", training)
        try:
            chapter = self.db.chapter.create(
                data={
                    'chapter_number': chapter_number,
                    'name': chapter_name,
                    'content': json_content_complete["content"],
                    'question': json_content_complete["question"],
                    'answers': Json(json_content_complete["responses"]),
                    'training': {'connect': {'id': training.id}},
                }
            )
            print("Chapter saved ", chapter)
        except PrismaError as pe:
            print(pe)

    def create_all_chapters(self, field: str, subject: str, training_json, training: Training):
        print('Creating chapters...')
        with ThreadPoolExecutor() as executor:
            for chapter in training_json:
                print("Creating chapter ", chapter["name"])
                executor.submit(self.create_chapter, field, subject,
                                training, int(chapter["id"]), chapter["name"])

    def create_and_add_to_db(self, field: str, subject: str):
        print('Creating training...')
        training_summary = self.openai_agent.create_training_summary(
            field, subject)
        if training_summary is None:
            raise ValueError("Training summary cannot be None")
        training_json: List[Dict[str, str]] = training_summary
        training: Training = self.db.training.create(
            data={
                'name': subject,
                'field': field,
                'description': "Training sur "+subject,
            }
        )
        self.create_all_chapters(field, subject, training_json, training)


def main():
    training_creator = TrainingCreator(mock=True)


if __name__ == "__main__":
    main()

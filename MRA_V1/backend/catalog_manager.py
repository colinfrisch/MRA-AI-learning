# training_manager.py
from prisma import Prisma
import json
from typing import List, Optional


class Answer:
    def __init__(self, text: str, valid: bool):
        self.text = text
        self.valid = valid

    def to_dict(self):
        return {"text": self.text, "valid": self.valid}

class Chapter:
    def __init__(self, chapter_id: int, name: str, content: str, question: str, answers: list[Answer], training_id: int):
        self.id = chapter_id
        self.name = name
        self.content = content
        self.question = question
        self.answers = answers
        self.training_id = training_id

    def get_answers(self) -> list[Answer]:
        return self.answers

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "content": self.content,
            "question": self.question,
            "answers": [answer.to_dict() for answer in self.answers],
            "training_id": self.training_id
        }

class Training:
    def __init__(self, training_id: int, name: str, field: str, description: str, chapters: Optional[List['Chapter']] = None):
        self.id = training_id
        self.name = name
        self.field = field
        self.description = description
        self.chapters = chapters if chapters is not None else []

    def get_name(self) -> str:
        return self.name

    def get_field(self) -> str:
        return self.field

    def get_description(self) -> str:
        return self.description

    def get_chapters(self) -> list[Chapter]:
        return self.chapters

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "field": self.field,
            "description": self.description,
            "chapters": [chapter.to_dict() for chapter in self.chapters]
        }


'''
Useful functions in TrainingManager:
- create_training(name: str, field: str, description: str) -> Training
- add_chapter_to_training(name: str, content: str, question: str, answers: list[dict], training_id: int) -> Chapter
- get_all_chapters_from_training(training_id: int) -> list[Chapter]
- get_all_trainings() -> list[Training]
- get_all_training_summaries() -> list[dict]
- get_all_training_summary_for_field(field: str) -> list[dict]
- get_training_by_id(training_id: int) -> Training
- modify_chapter_section(chapter_id: int,section:str, new_content:str)

'''

class TrainingManager:
    def __init__(self):
        self.db = Prisma()

    async def create_training(self, name: str, field: str, description: str) -> Training:
        training = await self.db.training.create(
            data={
                'name': name,
                'field': field,
                'description': description,
            }
        )
        return Training(training.id, name, field, description, [])

    async def add_chapter_to_training(self, name: str, content: str, question: str, answers: list[dict], training_id: int) -> Chapter:
        answers_json = json.dumps(answers)
        chapter = await self.db.chapter.create(
            data={
                'name': name,
                'content': content,
                'question': question,
                'answers': answers_json,
                'training_id': training_id,
            }
        )
        return Chapter(
            chapter.id,
            name,
            content,
            question,
            [Answer(ans["text"], ans["valid"]) for ans in answers],
            training_id
        )

    async def get_all_chapters_from_training(self, training_id: int) -> list[Chapter]:
        chapters = await self.db.chapter.find_many(where={'training_id': training_id})
        chapter_list = []
        for chapter in chapters:
            answers = json.loads(chapter.answers)
            chapter_list.append(Chapter(chapter.id, chapter.name, chapter.content, chapter.question, [Answer(ans["text"], ans["valid"]) for ans in answers], chapter.training_id))
        return chapter_list

    async def get_all_trainings(self) -> list[Training]:
        trainings = await self.db.training.find_many(include={'chapters': True})
        return [Training(training.id, training.name, training.field, training.description, 
                         [Chapter(chapter.id, chapter.name, chapter.content, chapter.question, 
                                  [Answer(resp["text"], resp["valid"]) for resp in json.loads(chapter.answers)], chapter.training_id) 
                          for chapter in training.chapters]) 
                for training in trainings]

    async def get_all_training_summaries(self) -> list[dict]:
        trainings = await self.db.training.find_many(select={'id': True, 'name': True, 'field': True, 'description': True})
        return [{'id': training.id, 'name': training.name, 'field': training.field, 'description': training.description} 
                for training in trainings]

    async def get_all_training_summary_for_field(self, field: str) -> list[dict]:
        all_summaries = await self.get_all_training_summaries()
        return [summary for summary in all_summaries if summary["field"] == field]

    async def get_training_by_id(self, training_id: int) -> Training:
        training = await self.db.training.find_unique(where={'id': training_id}, include={'chapters': True})
        if training:
            chapters = [Chapter(chapter.id, chapter.name, chapter.content, chapter.question, 
                                [Answer(resp["text"], resp["valid"]) for resp in json.loads(chapter.answers)], chapter.training_id) 
                        for chapter in training.chapters]
            return Training(training.id, training.name, training.field, training.description, chapters)
        return None

    async def modify_chapter_section(self, chapter_id: int, section: str, new_content: str):
        await self.db.chapter.update(
            where={'id': chapter_id},
            data={section: new_content}
        )

async def main():
    training_manager = TrainingManager()
    await training_manager.db.connect()
    new_training = await training_manager.create_training("Training 1", "history", "Description 1")
    training_id = new_training.to_dict()['id']
    print('training added')

    new_chap1 = await training_manager.add_chapter_to_training("Chapter 1", "Content 1", "Question 1", [{"text": 'qtxt1', "valid": True},{"text": 'qtxt2', "valid": False}], training_id)
    
    print('chapter added : ', new_chap1.to_dict()['name'])
    
    trainings = await training_manager.get_all_trainings()
    for training in trainings:
        print("Training Name:", training.get_name())
        print("Field:", training.get_field())
        print("Description:", training.get_description())
        for chapter in training.get_chapters():
            print("Chapter ID:", chapter.id)
            print("Name:", chapter.name)
            print("Content:", chapter.content)
            print("Question:", chapter.question)
            for answer in chapter.get_answers():
                print("answer:", answer.text, "Valid:", answer.valid)
    await training_manager.db.disconnect()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

import random
from typing import List, Optional
from prisma import Prisma
from prisma.models import User, Chapter, Training
from prisma.types import TrainingWhereUniqueInput
import json


class UserManager:
    def __init__(self):
        self.db = Prisma(log_queries=False)
        self.db.connect()

    def create_user(self, username, phone) -> User:
        return self.db.user.create(
            data={
                "username": username,
                "phone": phone,
            }
        )

    def get_user(self, user_id) -> User | None:
        return self.db.user.find_unique(
            where={"id": user_id}, include={"current_chapter": True}
        )

    def get_user_by_name(self, username) -> User | None:
        return self.db.user.find_unique(
            where={"username": username}, include={"current_chapter": True}
        )

    # add an eval to the current training chapter
    # and call next_chapter to change the current chapter
    # return the next chapter or None if it was the last chapter and the training is finished
    def add_eval_to_current_training_chapter(
        self, user, success: bool
    ) -> Optional[Chapter]:
        if not user:
            raise Exception("User not found")
        if not user.current_chapter:
            raise Exception("User has no current chapter")
        # save the score in the eval table
        self.db.eval.create(
            data={
                "user_id": user.id,
                "chapter_id": user.current_chapter.id,
                "score": 1 if success else 0,
            }
        )
        return self.next_chapter(user)

    # set the current chapter to the next one or finish the training
    # return the next chapter or None if it was the last chapter and the training is finished
    def next_chapter(self, user: User) -> Optional[Chapter]:
        # get the next
        if not user:
            raise Exception("User not found")
        current_chapter = user.current_chapter
        if not current_chapter:
            raise Exception("User has no current chapter")
        next_chapter_number = current_chapter.chapter_number + 1
        next_chapter = self.db.chapter.find_first(
            where={
                "training_id": current_chapter.training_id,
                "chapter_number": next_chapter_number,
            }
        )
        if not next_chapter:
            self.finish_current_training(user, current_chapter.training_id)
            return None

        # set the current chapter
        self.db.user.update(
            where={"id": user.id},
            data={"current_chapter": {"connect": {"id": next_chapter.id}}},
        )
        return next_chapter

    # set the current training chapter and return this chapter
    def set_current_training_chapter(self, user: User, chapter: Chapter) -> Chapter:
        self.db.user.update(
            where={"id": user.id},
            data={"current_chapter": {"connect": {"id": chapter.id}}},
        )
        return chapter

    # remove the current_chapter (training is finished)
    # add the training to the finished_trainings
    def finish_current_training(self, user: User, training_id):
        # remove the current_chapter (training is finished)
        self.db.user.update(
            where={"id": user.id}, data={"current_chapter": {"disconnect": True}}
        )
        # add the training to the finished_trainings

        user_with_trainings = self.db.user.find_first(
            where={"id": user.id}, include={"finished_trainings": True}
        )
        if user_with_trainings is None:
            raise Exception("User not found")

        f_trainings = user_with_trainings.finished_trainings or []
        # Convert the finished trainings to a list of TrainingWhereUniqueInput
        f_trainings_ids = [TrainingWhereUniqueInput(
            id=t.id) for t in f_trainings]
        f_trainings_ids.append(TrainingWhereUniqueInput(id=training_id))

        self.db.user.update(
            where={"id": user.id},
            data={"finished_trainings": {"connect": f_trainings_ids}},
        )
        if not user:
            raise Exception("User not found")

    # start the training setting up the current_chapter and returning this chapter
    def start_training(self, user: User, training: Training) -> Chapter:
        if not user:
            raise Exception("User not found")
        if not training:
            raise Exception("Training not found")
        # find the first chapter of the training (minimum chapter_number)
        first_chapter = self.db.chapter.find_first(
            where={"training_id": training.id}, order={"chapter_number": "asc"}
        )
        if not first_chapter:
            raise Exception("No chapters found for training")
        # set the current_chapter to the first chapter
        return self.set_current_training_chapter(user, first_chapter)

    def get_score_for_user(self, user: User) -> int:
        result = self.db.eval.group_by(
            by=["user_id"], where={"user_id": user.id}, sum={"score": True}
        )
        if result and "_sum" in result[0] and "score" in result[0]["_sum"]:
            return result[0]["_sum"]["score"]
        return 0

    def get_finised_trainings(self, user: User) -> List[Training]:
        user_with_trainings = self.db.user.find_first(
            where={"id": user.id}, include={"finished_trainings": True}
        )
        if user_with_trainings is None:
            return []
        return user_with_trainings.finished_trainings or []

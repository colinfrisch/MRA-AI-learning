import random
from prisma import Prisma 
from prisma.models import User, Chapter
import json

class UserManager:
    def __init__(self):
        self.db = Prisma(log_queries=False)
        self.db.connect()

    def create_user(self, username, phone) -> User:
        return self.db.user.create(
            data={
                'username': username,
                'phone': phone,
            }
        )
    
    def get_user(self, user_id) -> User:
        return self.db.user.find_unique(where={'id': user_id}, include={'current_chapter':True})

    def get_user_by_name(self, username) -> User:
        return self.db.user.find_unique(where={'username': username})

    # add an eval to the current training chapter
    # and call next_chapter to change the current chapter
    # return the next chapter or None if it was the last chapter and the training is finished
    def add_eval_to_current_training_chapter(self, user_id, success:bool) -> Chapter:
        user: User = self.db.user.find_unique(where={'id': user_id}, include={'current_chapter':True})
        if not user:
            raise Exception("User not found") 
        if not user.current_chapter:
            raise Exception("User has no current chapter")
        # save the score in the eval table
        self.db.eval.create(
            data={
                'user_id': user_id,
                'chapter_id': user.current_chapter.id,
                'score': 1 if success else 0
            }
        )
        return self.next_chapter(user)

    # set the current chapter to the next one or finish the training
    # return the next chapter or None if it was the last chapter and the training is finished
    def next_chapter(self, user: User) -> Chapter:
        if not user:
            raise Exception("User not found")
        current_chapter = user.current_chapter
        if not current_chapter:
            raise Exception("User has no current chapter")
        next_chapter_number = current_chapter.chapter_number + 1
        next_chapter = self.db.chapter.find_first(
            where={
                'training_id':  current_chapter.training_id,
                'chapter_number': next_chapter_number
            }
        )
        if not next_chapter:
            self.finish_current_training(user, current_chapter.training_id)
            return None

        # set the current chapter
        self.db.user.update(
            where={'id': user.id},
            data={'current_chapter': {'connect': {'id': next_chapter.id}}}
        )
        return next_chapter

    # set the current training chapter and return this chapter
    def set_current_training_chapter(self, user:User, chapter:Chapter) -> Chapter:
        self.db.user.update(
            where={'id': user.id},
            data={'current_chapter': {'connect': {'id': chapter.id}}}
        )
        return chapter

    # remove the current_chapter (training is finished)
    # add the training to the finished_trainings
    def finish_current_training(self, user:User, training_id):
        # remove the current_chapter (training is finished)
        self.db.user.update(
            where={'id': user.id},
            data={'current_chapter': {'disconnect':True}}
        )
        # add the training to the finished_trainings
        self.db.user.update(
            where={'id': user.id},
            data={'finished_trainings': {'connect': {'id': training_id}}}
        )
        if not user:
            raise Exception("User not found")
        
    # start the training setting up the current_chapter and returning this chapter
    def start_training(self, user_id, training_id) -> Chapter:
        user = self.get_user(user_id)
        if not user:
            raise Exception("User not found")
        training = self.db.training.find_unique(where={'id': training_id})
        if not training:
            raise Exception("Training not found")
        # find the first chapter of the training (minimum chapter_number)
        first_chapter = self.db.chapter.find_first(
            where={'training_id': training_id},
            order={'chapter_number': 'asc'}
        )
        if not first_chapter:
            raise Exception("No chapters found for training")
        # set the current_chapter to the first chapter
        return self.set_current_training_chapter(user, first_chapter)



def main():
    user_manager = UserManager()
    user  = user_manager.db.user.find_first()
    if not user:      
      user = user_manager.create_user("john_doe", "123-456-7890")
    
    print("find a traininig")
    training = user_manager.db.training.find_first(include={'chapters': True})
    print("training ", training)
    print("training chapters ", training.chapters)

    user=user_manager.get_user(user.id)
    print ("user ",user)

    print ("start the training")
    chapter = user_manager.start_training(user.id, training.id)
    user=user_manager.get_user(user.id)
    print ("user ",user)
 
    # iterate over the chapters until one is None
    while chapter:
        print("The current chapter is ", chapter)
        success = random.choice([True, False])
        print(f"add eval {success} to current chapter : ", chapter)
        chapter = user_manager.add_eval_to_current_training_chapter(user.id, success)

    print("The training is finished")
    user=user_manager.get_user(user.id)
    print ("user ",user)
   
    user_manager.db.disconnect()


if __name__ == "__main__":
    main()

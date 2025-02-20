import unittest
import random
from backend.training_creator import TrainingCreator
from backend.user_manager import UserManager
from prisma.models import User, Training, Chapter
from prisma import Prisma

test_username="test_doe"

class TestUserManager(unittest.TestCase):

    def setUp(self):
        self.user_manager = UserManager()
        self.training_creator = TrainingCreator(mock=True)

    def test_main_simulation(self):
        db : Prisma = self.user_manager.db 
        # create a user if necessary and cleanup the eval and current chapter     
        user = db.user.find_first(where={'username':test_username})
        if not user:
            user = self.user_manager.create_user(test_username, "123-456-7890")
        else:
            # remove eval, trainings...
            db.eval.delete_many(where={'user_id':user.id})
            db.user.update(where={'id':user.id}, data= {'current_chapter':{'disconnect':True}})
            
        self.assertIsNotNone(user, "User creation failed")

        # find a valid training
        print("find a training")
        training = db.training.find_first(include={'chapters': True})
        if not training:
            self.training_creator.check_trainings()
            training = db.training.find_first(include={'chapters': True})
        self.assertIsNotNone(training, "Training not found")
        self.assertTrue(len(training.chapters) > 0, "Training has no chapters")

        # start the training
        chapter = self.user_manager.start_training(user, training)
        self.assertIsNotNone(chapter, "Failed to start training: no chapter found")

        # iterate over the chapters until one is None
        score=0
        nb_chapter=0
        while chapter:
          # check that the user's current chapter is correct
          user = self.user_manager.get_user(user.id)
          self.assertEqual(user.current_chapter_id, chapter.id, "user's current_chapter has not been updated")
          # check the the eval is correct
          success = random.choice([True, False])
          nb_chapter=nb_chapter+1
          score =  score+1 if success else score
          chapter = self.user_manager.add_eval_to_current_training_chapter(user, success)
          self.assertEqual(db.eval.count(where={'user_id':user.id}), nb_chapter,"Invalid number of evals")

        # training is finished
        user = self.user_manager.get_user(user.id)
        self.assertIsNone(user.current_chapter, "User still has a current chapter after finishing training")
        self.assertEqual(self.user_manager.get_score_for_user(user), score, "Score don't match")

        #self.assertTrue(self.user_manager.get_finised_trainings(user).index(training))

    def tearDown(self):
        db : Prisma = self.user_manager.db 
        user = db.user.find_first(where={'username':test_username})
        if user:
            # remove evals and user
            db.eval.delete_many(where={'user_id':user.id})
            db.user.delete(where={'id':user.id})

        self.user_manager.db.disconnect()

if __name__ == "__main__":
    unittest.main()
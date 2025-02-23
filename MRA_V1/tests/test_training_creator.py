import unittest
from unittest.mock import patch
from backend.training_creator import TrainingCreator
from prisma import Prisma


class TestTrainingCreator(unittest.TestCase):
    """
    Unit tests for the TrainingCreator class.

    This test suite ensures that the TrainingCreator class correctly interacts
    with the Prisma database and the OpenAIAgent to create and manage training
    and chapter content.
    """

    @patch("backend.training_creator.OpenAIAgent")
    def setUp(self, MockOpenAIAgent):
        """
        Set up the test environment.

        This method is called before each test. It initializes the TrainingCreator
        and Prisma instances, mocks the OpenAIAgent, and ensures the database is empty.
        """
        self.training_creator = TrainingCreator()
        self.db = Prisma()
        self.db.connect()
        # Mock the OpenAIAgent
        mock_agent = MockOpenAIAgent.return_value
        self.setupMockOpenAIAgent(mock_agent)
        # Ensure the database is empty
        self.db.training.delete_many()
        self.db.chapter.delete_many()

    @staticmethod
    def setupMockOpenAIAgent(mock_agent):
        """
        Set up the mock OpenAIAgent.

        This method configures the mock OpenAIAgent to return predefined values
        for create_chapter_content and create_training_content methods.
        """
        mock_agent.create_chapter_content.return_value = {
            "content": "Blah Blah Blah",
            "question": "Chat do you think of blah?",
            "responses": [
                {"text": "Texte de la réponse 1", "valid": 1},
                {"text": "Texte de la réponse 2", "valid": 0},
                {"text": "Texte de la réponse 3", "valid": 0},
                {"text": "Texte de la réponse 4", "valid": 0},
                {"text": "Texte de la réponse 5", "valid": 0},
            ],
        }
        mock_agent.create_training_summary.return_value = [
            {"id": "1", "name": "Tendinite"},
            {"id": "2", "name": "Genou"},
            {"id": "3", "name": "Tendinite au genou"},
        ]

    def tearDown(self):
        """
        Tear down the test environment.

        This method is called after each test. It ensures the database is empty
        and disconnects from the Prisma instance.
        """
        self.db.training.delete_many()
        self.db.disconnect()

    def test_check_trainings_creates_initial_training(self):
        """
        Test that check_trainings creates the initial training.

        This test verifies that the check_trainings method of the TrainingCreator
        class correctly creates an initial training with the expected properties
        and associated chapters.
        """
        self.training_creator.check_trainings()

        # Check that a training has been created
        training = self.db.training.find_first(include={"chapters": True})
        self.assertIsNotNone(training)
        if training:
            self.assertEqual(training.name, "Tendinite rotulienne")
            self.assertEqual(training.field, "Médecine")
            self.assertEqual(training.description, "Training sur Tendinite rotulienne")
            self.assertIsNotNone(training.chapters)
            if training.chapters:
                self.assertEqual(len(training.chapters), 3)
                self.assertEqual(training.chapters[0].name, "Tendinite")
                self.assertEqual(training.chapters[1].name, "Genou")
                self.assertEqual(training.chapters[2].name, "Tendinite au genou")
                self.assertEqual(training.chapters[0].training_id, training.id)
                self.assertEqual(training.chapters[1].training_id, training.id)
                self.assertEqual(training.chapters[2].training_id, training.id)
                self.assertEqual(training.chapters[0].chapter_number, 1)
                self.assertEqual(training.chapters[1].chapter_number, 2)
                self.assertEqual(training.chapters[2].chapter_number, 3)
                self.assertEqual(training.chapters[0].content, "Blah Blah Blah")
                self.assertEqual(
                    training.chapters[0].question, "Chat do you think of blah?"
                )
                self.assertIsNotNone(training.chapters[0].answers)
                if training.chapters[0].answers:
                    self.assertEqual(len(training.chapters[0].answers), 5)

    def test_create_and_add_to_db(self):
        """
        Test that create_and_add_to_db creates a training and adds it to the database.

        This test verifies that the create_and_add_to_db method of the TrainingCreator
        class correctly creates a training with the specified field and subject, and
        adds it to the database with the expected properties and associated chapters.
        """
        field = "Geometry"
        subject = "Pythagorean theorem"

        self.training_creator.create_and_add_to_db(field, subject)

        # Check that the training has been created
        training = self.db.training.find_first(
            where={"name": subject}, include={"chapters": True}
        )
        self.assertIsNotNone(training)
        if training:
            self.assertEqual(training.name, subject)
            self.assertEqual(training.field, field)

            # Check that chapters have been created
            chapters = self.db.chapter.find_many(where={"training_id": training.id})
            self.assertEqual(len(chapters), 3)


if __name__ == "__main__":
    unittest.main()

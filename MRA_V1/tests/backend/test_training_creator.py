import unittest
from unittest.mock import patch, MagicMock
from backend.training_creator import TrainingCreator
from prisma.models import Training

class TestTrainingCreator(unittest.TestCase):

    @patch('backend.training_creator.OpenAIAgent')
    def setUp(self, MockOpenAIAgent):
        self.mock_openai_agent = MockOpenAIAgent.return_value
        self.training_creator = TrainingCreator(mock=True)

    def test_create_and_add_to_db(self):
        self.mock_openai_agent.create_training_summary.return_value = [
            {"id": "1", "name": "Chapter 1"},
            {"id": "2", "name": "Chapter 2"}
        ]
        self.mock_prisma.training.create.return_value = MagicMock(spec=Training, id=1)

        self.training_creator.create_and_add_to_db("Field", "Subject")

        self.mock_openai_agent.create_training_summary.assert_called_once_with("Field", "Subject")
        self.mock_prisma.training.create.assert_called_once_with(
            data={
                'name': 'Subject',
                'field': 'Field',
                'description': 'Training sur Subject',
            }
        )
        self.mock_prisma.chapter.create.assert_any_call(
            data={
                'chapter_number': 1,
                'name': 'Chapter 1',
                'content': self.mock_openai_agent.create_chapter_content.return_value["content"],
                'question': self.mock_openai_agent.create_chapter_content.return_value["question"],
                'answers': self.mock_openai_agent.create_chapter_content.return_value["responses"],
                'training': {'connect': {'id': 1}},
            }
        )
        self.mock_prisma.chapter.create.assert_any_call(
            data={
                'chapter_number': 2,
                'name': 'Chapter 2',
                'content': self.mock_openai_agent.create_chapter_content.return_value["content"],
                'question': self.mock_openai_agent.create_chapter_content.return_value["question"],
                'answers': self.mock_openai_agent.create_chapter_content.return_value["responses"],
                'training': {'connect': {'id': 1}},
            }
        )

if __name__ == '__main__':
    unittest.main()
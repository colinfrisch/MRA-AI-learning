from prisma import Prisma
from prisma.models import Training


class TrainingManager:
    def __init__(self):
        self.db = Prisma()
        self.db.connect()

    def create_training(self, name: str, field: str, description: str) -> Training:
        return self.db.training.create(
            data={
                "name": name,
                "field": field,
                "description": description,
            }
        )

    def get_all_trainings(self) -> list[Training]:
        return self.db.training.find_many(include={"chapters": True})

    def get_all_training_summaries(self) -> list[Training]:
        return self.db.training.find_many()

    def get_all_training_summary_for_field(self, field: str) -> list[Training]:
        return self.db.training.find_many(
            where={"field": field},
        )

    def get_training_by_id(self, training_id: int) -> Training | None:
        return self.db.training.find_unique(
            where={"id": int(training_id)}, include={"chapters": True}
        )

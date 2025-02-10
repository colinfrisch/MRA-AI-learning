from prisma import Prisma 
import json

class CurrentTraining:
    def __init__(self, training_id: str, chapters_done: list[str]):
        self.training_id = training_id
        self.chapters_done = chapters_done

    def get_training_id(self) -> str:
        return self.training_id

    def get_chapters_done(self) -> list[str]:
        return self.chapters_done

class User:
    def __init__(self, user_id, username, phone, current_training, finished_training):
        self.id = user_id
        self.username = username
        self.phone = phone
        self.current_training = current_training
        self.finished_training = finished_training

    def get_finished_training(self) -> list[str]:
        return self.finished_training

    def get_current_training(self) -> CurrentTraining:
        return self.current_training

class UserManager:
    def __init__(self):
        self.db = Prisma()

    async def create_user(self, username, phone):
        user = await self.db.user.create(
            data={
                'username': username,
                'phone': phone,
                'current_training': None,
            }
        )
        return User(user.id, user.username, user.phone, None, None)
    
    async def get_user(self, user_id) -> User:
        user = await self.db.user.find_unique(where={'id': user_id})
        if user:
            current_training_data = json.loads(user.current_training) if user.current_training else {"training_id": "", "chapters_done": []}
            current_training = CurrentTraining(current_training_data["training_id"], current_training_data["chapters_done"])
            finished_training = json.loads(user.finished_training) if user.finished_training else []
            return User(user.id, user.username, user.phone, current_training, finished_training)
        return None

    async def get_user_by_name(self, username) -> User:
        user = await self.db.user.find_unique(where={'username': username})
        if user:
            current_training_data = json.loads(user.current_training) if user.current_training else {"training_id": "", "chapters_done": []}
            current_training = CurrentTraining(current_training_data["training_id"], current_training_data["chapters_done"])
            finished_training = json.loads(user.finished_training) if user.finished_training else []
            return User(user.id, user.username, user.phone, current_training, finished_training)
        return None

    async def set_current_training(self, user_id, training_id):
        current_training = json.dumps({"training_id": training_id, "chapters_done": []})
        await self.db.user.update(
            where={'id': user_id},
            data={'current_training': current_training}
        )

    async def add_chapter_done(self, user_id, chapter_id):
        user = await self.db.user.find_unique(where={'id': user_id})
        if user and user.current_training:
            current_training_data = json.loads(user.current_training)
            current_training_data["chapters_done"].append(chapter_id)
            current_training = json.dumps(current_training_data)
            await self.db.user.update(
                where={'id': user_id},
                data={'current_training': current_training}
            )

    async def set_chapter_finished(self, user_id, chapter_id, success):
        user = await self.db.user.find_unique(where={'id': user_id})
        if user and user.current_training:
            current_training_data = json.loads(user.current_training)
            current_training_data["chapters_done"].append(chapter_id)
            current_training = json.dumps(current_training_data)
            await self.db.user.update(
                where={'id': user_id},
                data={'current_training': current_training}
            )

async def main():
    user_manager = UserManager()
    await user_manager.db.connect()
    await user_manager.create_user("john_doe", "123-456-7890")
    await user_manager.set_current_training(1, "training_123")
    await user_manager.add_chapter_done(1, "chapter_1")
    await user_manager.add_chapter_done(1, "chapter_2")
    user = await user_manager.get_user(1)
    if user:
        print("Username:", user.username)
        print("Phone:", user.phone)
        print("Current Training:", user.get_current_training().__dict__)
        print("Finished Training:", user.get_finished_training())
    await user_manager.db.disconnect()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
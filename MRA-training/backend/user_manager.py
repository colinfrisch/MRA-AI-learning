from backend.db import DBConnection
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
    def __init__(self, user_id, username, email, current_training, finished_training):
        self.id = user_id
        self.username = username
        self.email = email
        self.current_training = current_training
        self.finished_training = finished_training

    def get_finished_training(self) -> list[str]:
        return self.finished_training

    def get_current_training(self) -> CurrentTraining:
        return self.current_training

class UserManager:
    def create_user(self, username, email):
        with DBConnection() as db:
            db.execute("INSERT INTO users (username, email) VALUES (?, ?)", (username, email))
            db.commit()

    def get_user(self, user_id) -> User:
        with DBConnection() as db:
            db.execute("SELECT * FROM users WHERE id = ?", (user_id,))
            row = db.fetchone()
            if row:
                current_training_data = json.loads(row["current_training"]) if row["current_training"] else {"training_id": "", "chapters_done": []}
                current_training = CurrentTraining(current_training_data["training_id"], current_training_data["chapters_done"])
                finished_training = json.loads(row["finished_training"]) if row["finished_training"] else []
                return User(row["id"], row["username"], row["email"], current_training, finished_training)
            return None

    def set_current_training(self, user_id, training_id):
        with DBConnection() as db:
            current_training = json.dumps({"training_id": training_id, "chapters_done": []})
            db.execute("UPDATE users SET current_training = ? WHERE id = ?", (current_training, user_id))
            db.commit()

    def add_chapter_done(self, user_id, chapter_id):
        with DBConnection() as db:
            db.execute("SELECT current_training FROM users WHERE id = ?", (user_id,))
            row = db.fetchone()
            if row and row["current_training"]:
                current_training_data = json.loads(row["current_training"])
                current_training_data["chapters_done"].append(chapter_id)
                current_training = json.dumps(current_training_data)
                db.execute("UPDATE users SET current_training = ? WHERE id = ?", (current_training, user_id))
                db.commit()

def main():
    user_manager = UserManager()
    user_manager.create_user("john_doe", "john@example.com")
    user_manager.set_current_training(1, "training_123")
    user_manager.add_chapter_done(1, "chapter_1")
    user_manager.add_chapter_done(1, "chapter_2")
    user = user_manager.get_user(1)
    if user:
        print("Username:", user.username)
        print("Current Training:", user.get_current_training().__dict__)
        print("Finished Training:", user.get_finished_training())

if __name__ == "__main__":
    main()
# runit via : python -m backend.init_db
from backend.db import DBConnection

def init_db():
    """
    Reads schema.sql and executes all statements to initialize/reset the DB.
    """
    # Path to your SQL file. Adjust if your file is in a different location.
    schema_file = "backend/schema.sql"
    
    # Read the entire script into a variable
    with open(schema_file, "r", encoding="utf-8") as f:
        sql_script = f.read()

    # Use DBConnection context manager
    with DBConnection() as db:
        # executescript() runs multiple statements from a single string
        db.conn.executescript(sql_script)
        db.commit()
        print("Database initialized using schema.sql!")

if __name__ == "__main__":
    init_db()

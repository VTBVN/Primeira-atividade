import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / 'banco.db'


class Note:
    def __init__(self, id, title, content, favorite=0):
        self.id = id
        self.title = title
        self.content = content
        self.favorite = favorite


def row_to_note(row):
    return Note(
        id=row['id'],
        title=row['title'],
        content=row['content'],
        favorite=row['favorite'],
    )


def initialize_database():
    connection = sqlite3.connect(DB_PATH)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS note (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL
        )
    """)

    columns = [
        row[1]
        for row in connection.execute("PRAGMA table_info(note)").fetchall()
    ]

    if 'favorite' not in columns:
        connection.execute(
            "ALTER TABLE note ADD COLUMN favorite INTEGER NOT NULL DEFAULT 0"
        )

    connection.commit()
    connection.close()


def get_connection():
    initialize_database()

    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def load_notes():
    connection = get_connection()

    rows = connection.execute("""
        SELECT id, title, content, favorite
        FROM note
        ORDER BY favorite DESC, id
    """).fetchall()

    connection.close()

    return [row_to_note(row) for row in rows]


def load_note(note_id):
    connection = get_connection()

    row = connection.execute(
        """
        SELECT id, title, content, favorite
        FROM note
        WHERE id = ?
        """,
        (note_id,),
    ).fetchone()

    connection.close()

    if row is None:
        return None

    return row_to_note(row)


def create_note(title, content):
    connection = get_connection()

    connection.execute(
        'INSERT INTO note (title, content) VALUES (?, ?)',
        (title, content),
    )

    connection.commit()
    connection.close()


def update_note(note_id, title, content):
    connection = get_connection()

    connection.execute(
        'UPDATE note SET title = ?, content = ? WHERE id = ?',
        (title, content, note_id),
    )

    connection.commit()
    connection.close()


def delete_note(note_id):
    connection = get_connection()

    connection.execute(
        'DELETE FROM note WHERE id = ?',
        (note_id,),
    )

    connection.commit()
    connection.close()


def toggle_favorite(note_id):
    connection = get_connection()

    connection.execute(
        """
        UPDATE note
        SET favorite = CASE favorite WHEN 1 THEN 0 ELSE 1 END
        WHERE id = ?
        """,
        (note_id,),
    )

    connection.commit()
    connection.close()


def load_template(filename):
    with open(BASE_DIR / "static" / "templates" / filename, encoding="utf-8") as file:
        return file.read()

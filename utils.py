import json
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / 'banco.db'
LEGACY_NOTES_FILE = BASE_DIR / 'static' / 'data' / 'notes.json'


class Note:
    def __init__(self, id, title, content, favorite=0):
        self.id = id
        self.title = title
        self.content = content
        self.favorite = favorite


def configure_database(database=None, legacy_notes_file=None):
    global DB_PATH, LEGACY_NOTES_FILE

    if database is not None:
        DB_PATH = Path(database)

    if legacy_notes_file is not None:
        LEGACY_NOTES_FILE = Path(legacy_notes_file)


def row_to_note(row):
    return Note(
        id=row['id'],
        title=row['title'],
        content=row['content'],
        favorite=row['favorite'],
    )


def initialize_database(database=None, legacy_notes_file=None):
    db_path = Path(database) if database is not None else DB_PATH
    legacy_path = Path(legacy_notes_file) if legacy_notes_file is not None else LEGACY_NOTES_FILE

    connection = sqlite3.connect(db_path)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS note (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL
        )
    """)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS app_meta (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL
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

    imported = connection.execute(
        "SELECT value FROM app_meta WHERE key = 'legacy_imported'"
    ).fetchone()

    if imported is None:
        if legacy_path is not None and legacy_path.exists():
            notes = json.loads(legacy_path.read_text(encoding='utf-8'))
            for note in notes:
                title = note.get('title', note.get('titulo', ''))
                content = note.get('content', note.get('detalhes', ''))
                if str(title).strip() and str(content).strip():
                    connection.execute(
                        'INSERT INTO note (title, content) VALUES (?, ?)',
                        (title, content),
                    )

        connection.execute(
            "INSERT INTO app_meta (key, value) VALUES ('legacy_imported', '1')"
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
    if title is None or content is None or not title.strip() or not content.strip():
        return False

    connection = get_connection()

    connection.execute(
        'INSERT INTO note (title, content) VALUES (?, ?)',
        (title, content),
    )

    connection.commit()
    connection.close()
    return True


def update_note(note_id, title, content):
    if title is None or content is None or not title.strip() or not content.strip():
        return False

    connection = get_connection()

    cursor = connection.execute(
        'UPDATE note SET title = ?, content = ? WHERE id = ?',
        (title, content, note_id),
    )

    connection.commit()
    updated = cursor.rowcount > 0
    connection.close()
    return updated


def delete_note(note_id):
    connection = get_connection()

    cursor = connection.execute(
        'DELETE FROM note WHERE id = ?',
        (note_id,),
    )

    connection.commit()
    deleted = cursor.rowcount > 0
    connection.close()
    return deleted


def toggle_favorite(note_id):
    connection = get_connection()

    cursor = connection.execute(
        """
        UPDATE note
        SET favorite = CASE favorite WHEN 1 THEN 0 ELSE 1 END
        WHERE id = ?
        """,
        (note_id,),
    )

    connection.commit()
    updated = cursor.rowcount > 0
    connection.close()
    return updated


def load_template(filename):
    with open(BASE_DIR / "static" / "templates" / filename, encoding="utf-8") as file:
        return file.read()

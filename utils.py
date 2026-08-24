import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


def get_connection():
    connection = sqlite3.connect(BASE_DIR / 'banco.db')
    connection.row_factory = sqlite3.Row
    return connection


def load_notes():
    connection = get_connection()

    notes = connection.execute("""
        SELECT id, title, content
        FROM note
        ORDER BY id
    """).fetchall()

    connection.close()

    return notes


def load_template(filename):
    with open(BASE_DIR / "static" / "templates" / filename, encoding="utf-8") as file:
        return file.read()
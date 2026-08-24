from html import escape

from utils import (
    create_note,
    delete_note,
    load_note,
    load_notes,
    load_template,
    toggle_favorite,
    update_note,
)


def index():
    note_template = load_template('components/note.html')

    notes_li = [
        note_template.format(
            id=note.id,
            title=escape(note.title),
            details=escape(note.content),
            favorite_symbol='★' if note.favorite else '☆',
        )
        for note in load_notes()
    ]

    return load_template('index.html').format(
        notes=chr(10).join(notes_li)
    )


def submit(titulo, detalhes):
    create_note(titulo, detalhes)


def delete(note_id):
    delete_note(note_id)


def edit_page(note_id):
    note = load_note(note_id)

    if note is None:
        return index()

    return load_template('edit.html').format(
        id=note.id,
        title=escape(note.title, quote=True),
        details=escape(note.content, quote=True),
    )


def update(note_id, titulo, detalhes):
    update_note(note_id, titulo, detalhes)


def favorite(note_id):
    toggle_favorite(note_id)

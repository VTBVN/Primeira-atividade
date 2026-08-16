from utils import load_data, load_template, save_data

def index():
    note_template = load_template('components/note.html')
    notes_li = [note_template.format(title=d['titulo'], details=d['detalhes']) for d in load_data('notes.json')]
    return load_template('index.html').format(notes='\n'.join(notes_li))

def submit(titulo, detalhes):
    notes = load_data('notes.json')
    notes.append({
        'titulo': titulo,
        'detalhes': detalhes,
    })
    save_data('notes.json', notes)

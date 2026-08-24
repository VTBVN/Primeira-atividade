from flask import Flask, render_template_string, request, redirect
import views


app = Flask(__name__)

# Configurando a pasta de arquivos estaticos
app.static_folder = 'static'


@app.route('/')
def index():
    return render_template_string(views.index())


@app.route('/submit', methods=['POST'])
def submit_form():
    titulo = request.form.get('titulo')
    detalhes = request.form.get('detalhes')

    views.submit(titulo, detalhes)
    return redirect('/')


@app.route('/delete/<int:note_id>')
def delete_note(note_id):
    views.delete(note_id)
    return redirect('/')


@app.route('/update/<int:note_id>')
@app.route('/edit/<int:note_id>')
def edit_note(note_id):
    return render_template_string(views.edit_page(note_id))


@app.route('/update', methods=['POST'])
def update_note():
    note_id = request.form.get('id')
    titulo = request.form.get('titulo')
    detalhes = request.form.get('detalhes')

    views.update(note_id, titulo, detalhes)
    return redirect('/')


@app.route('/favorite/<int:note_id>')
def favorite_note(note_id):
    views.favorite(note_id)
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)

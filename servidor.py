from flask import Flask, render_template_string, request, redirect, abort
import views
from utils import configure_database, initialize_database


def create_app(test_config=None):
    app = Flask(__name__)
    app.static_folder = 'static'

    app.config.from_mapping(
        DATABASE='banco.db',
        LEGACY_NOTES_FILE=None,
    )

    if test_config is not None:
        app.config.update(test_config)

    configure_database(
        app.config.get('DATABASE'),
        app.config.get('LEGACY_NOTES_FILE'),
    )
    initialize_database(
        app.config.get('DATABASE'),
        app.config.get('LEGACY_NOTES_FILE'),
    )

    @app.route('/')
    def index():
        return render_template_string(views.index())

    @app.route('/submit', methods=['POST'])
    def submit_form():
        titulo = request.form.get('titulo')
        detalhes = request.form.get('detalhes')

        if not views.submit(titulo, detalhes):
            abort(400)

        return redirect('/')

    @app.route('/delete/<int:note_id>', methods=['GET', 'POST'])
    def delete_note(note_id):
        if not views.delete(note_id):
            abort(404)
        return redirect('/')

    @app.route('/update/<int:note_id>')
    @app.route('/edit/<int:note_id>')
    def edit_note(note_id):
        response = views.edit_page(note_id)
        if response is None:
            abort(404)
        return render_template_string(response)

    @app.route('/update', methods=['POST'])
    def update_note():
        note_id = request.form.get('id')
        titulo = request.form.get('titulo')
        detalhes = request.form.get('detalhes')

        if not views.update(note_id, titulo, detalhes):
            abort(404)

        return redirect('/')

    @app.route('/edit/<int:note_id>', methods=['POST'])
    def update_note_by_id(note_id):
        titulo = request.form.get('titulo')
        detalhes = request.form.get('detalhes')

        if not views.update(note_id, titulo, detalhes):
            abort(404)

        return redirect('/')

    @app.route('/favorite/<int:note_id>', methods=['GET', 'POST'])
    def favorite_note(note_id):
        if not views.favorite(note_id):
            abort(404)
        return redirect('/')

    return app


app = create_app()


if __name__ == '__main__':
    app.run(debug=True)

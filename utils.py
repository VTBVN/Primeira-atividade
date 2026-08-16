import json


def load_data(filename):
    """Carrega um arquivo JSON localizado em static/data."""
    with open(f"static/data/{filename}", encoding="utf-8") as file:
        return json.load(file)


def save_data(filename, data):
    """Salva dados em um arquivo JSON localizado em static/data."""
    with open(f"static/data/{filename}", "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


def load_template(filename):
    with open(f"static/templates/{filename}", encoding="utf-8") as file:
        return file.read()

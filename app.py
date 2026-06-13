from flask import Flask, request, render_template

app = Flask(__name__)

# Маршрут для главной страницы
@app.route('/')
def index():
    return "<h1>Заметки с тегами</h1><p>Прототип запущен</p>"

# Маршрут для добавления заметки
@app.route('/add', methods=['GET', 'POST'])
def add():
    return "Страница добавления заметки"

# Маршрут для редактирования
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    return f"Редактирование заметки номер {id}"

# Маршрут для удаления
@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    return f"Удаление заметки номер {id}"

if __name__ == '__main__':
    app.run(debug=True)
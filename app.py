from flask import Flask, request, render_template
import sqlite3

app = Flask(__name__)

# Маршрут для главной страницы
@app.route('/')
def index():
    conn = get_db()
    notes = conn.execute('SELECT * FROM notes').fetchall()
    conn.close()
    return render_template('index.html', notes=notes)

def get_db():
    conn = sqlite3.connect('notes.db')
    conn.execute('CREATE TABLE IF NOT EXISTS notes (id INTEGER PRIMARY KEY, title TEXT, content TEXT, tags TEXT)')
    return conn

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        tags = request.form['tags']
        
        conn = get_db()
        conn.execute('INSERT INTO notes (title, content, tags) VALUES (?, ?, ?)', (title, content, tags))
        conn.commit()
        conn.close()
        return "Заметка сохранена! <a href='/'>Назад</a>"
        
    return render_template('add.html')

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
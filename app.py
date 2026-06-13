from flask import Flask, request, render_template, redirect
import sqlite3
from datetime import datetime

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect('notes.db')
    conn.execute('''CREATE TABLE IF NOT EXISTS notes (
        id INTEGER PRIMARY KEY, 
        title TEXT, 
        content TEXT, 
        tags TEXT,
        created_date TEXT
    )''')
    return conn

@app.route('/')
def index():
    tag_filter = request.args.get('tag')
    conn = get_db()
    
    if tag_filter:
        # Ищем заметки, которые СОДЕРЖАТ этот тег
        notes = conn.execute(
            'SELECT * FROM notes WHERE tags LIKE ?', 
            (f'%{tag_filter}%',)
        ).fetchall()
    else:
        notes = conn.execute('SELECT * FROM notes').fetchall()
    
    # Считаем количество использований каждого тега (для облака)
    tag_counts = {}
    for note in notes:
        if note[3]:  # поле tags
            for tag in note[3].split():
                tag_counts[tag] = tag_counts.get(tag, 0) + 1
    
    # Сортируем теги по популярности
    all_tags = sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)
    
    conn.close()
    return render_template('index.html', notes=notes, all_tags=all_tags)

@app.route('/search')
def search():
    query = request.args.get('q', '')
    conn = get_db()
    
    if query:
        # Поиск по заголовку ИЛИ по тексту
        notes = conn.execute(
            'SELECT * FROM notes WHERE title LIKE ? OR content LIKE ?',
            (f'%{query}%', f'%{query}%')
        ).fetchall()
        
        # Считаем теги для результатов поиска
        tag_counts = {}
        for note in notes:
            if note[3]:
                for tag in note[3].split():
                    tag_counts[tag] = tag_counts.get(tag, 0) + 1
        all_tags = sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)
    else:
        notes = []
        all_tags = []
    
    conn.close()
    return render_template('index.html', notes=notes, all_tags=all_tags)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        tags = request.form['tags']
        # Получаем текущую дату и время
        date = datetime.now().strftime('%d.%m.%Y %H:%M')
        
        conn = get_db()
        conn.execute(
            'INSERT INTO notes (title, content, tags, created_date) VALUES (?, ?, ?, ?)', 
            (title, content, tags, date)
        )
        conn.commit()
        conn.close()
        return redirect('/')
    return render_template('add.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    conn = get_db()
    if request.method == 'POST':
        conn.execute(
            'UPDATE notes SET title=?, content=?, tags=? WHERE id=?', 
            (request.form['title'], request.form['content'], request.form['tags'], id)
        )
        conn.commit()
        conn.close()
        return redirect('/')
    
    note = conn.execute('SELECT * FROM notes WHERE id = ?', (id,)).fetchone()
    conn.close()
    return render_template('edit.html', note=note)

@app.route('/delete/<int:id>')
def delete(id):
    conn = get_db()
    conn.execute('DELETE FROM notes WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
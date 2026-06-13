import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from app import app

@pytest.fixture
def client():
    """Создание тестового клиента"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_main_page(client):
    """Тест 1: Главная страница возвращает 200"""
    response = client.get('/')
    assert response.status_code == 200

def test_add_note_page(client):
    """Тест 2: Страница добавления существует"""
    response = client.get('/add')
    assert response.status_code == 200

def test_add_note(client):
    """Тест 3: Добавление заметки"""
    response = client.post('/add', data={
        'title': 'Тест',
        'content': 'Тестовый контент',
        'tags': 'тест работа'
    }, follow_redirects=True)
    assert response.status_code == 200

def test_edit_page(client):
    """Тест 4: Страница редактирования"""
    # Сначала добавим заметку
    client.post('/add', data={
        'title': 'Для редактирования',
        'content': 'Контент',
        'tags': 'тест'
    })
    response = client.get('/edit/1')
    assert response.status_code == 200

def test_delete_note(client):
    """Тест 5: Удаление заметки"""
    # Добавляем заметку
    client.post('/add', data={
        'title': 'Для удаления',
        'content': 'Будет удалена',
        'tags': 'удалить'
    })
    # Удаляем
    response = client.get('/delete/1', follow_redirects=True)
    assert response.status_code == 200

def test_search_functionality(client):
    """Тест 6: Поиск по заголовку и тексту"""
    # Добавляем заметки
    client.post('/add', data={
        'title': 'Работа проект',
        'content': 'Важный проект',
        'tags': 'работа'
    })
    client.post('/add', data={
        'title': 'Личное дело',
        'content': 'Личные заметки',
        'tags': 'личное'
    })
    
    # Ищем по слову "проект"
    response = client.get('/search?q=проект')
    assert response.status_code == 200
    assert b'Работа проект' in response.data

def test_filter_by_tag(client):
    """Тест 7: Фильтрация по тегу"""
    # Добавляем заметки с разными тегами
    client.post('/add', data={
        'title': 'Заметка 1',
        'content': 'Текст 1',
        'tags': 'работа'
    })
    client.post('/add', data={
        'title': 'Заметка 2',
        'content': 'Текст 2',
        'tags': 'личное'
    })
    
    # Фильтруем по тегу "работа"
    response = client.get('/?tag=работа')
    assert response.status_code == 200
    assert b'Заметка 1' in response.data
import sqlite3  # Импортируем библиотеку для работы с базой данных SQLite
from flask import Flask, render_template, request, redirect, url_for  # Импортируем необходимые функции из Flask
from enum import Enum  # Импортируем Enum для создания перечислений действий

# Инициализация базы данных
db_path = "animals.db"  # Указываем путь к файлу базы данных

def init_db():
    # Создаем соединение с базой данных и создаем таблицу, если ее еще нет
    with sqlite3.connect(db_path) as con:
        con.execute('''CREATE TABLE IF NOT EXISTS animals
                       (id INTEGER PRIMARY KEY, name TEXT, description TEXT)''')

# Универсальная функция для работы с базой данных
def query_db(query, args=(), one=False):
    # Выполняем SQL-запрос и возвращаем результат
    with sqlite3.connect(db_path) as con:
        cur = con.execute(query, args)  # Выполняем запрос с аргументами
        rv = cur.fetchall()  # Получаем все результаты запроса
        return (rv[0] if rv else None) if one else rv  # Возвращаем один или все результаты

# Enum для действий (например, добавление, редактирование и т.д.)
class Action(Enum):
    ADD = 'Add'
    EDIT = 'Edit'
    DELETE = 'Delete'
    SHOW = 'Show'
    SEARCH = 'Search'
    CLEAR = 'Clear'
    EXIT = 'Exit'

# Инициализация Flask-приложения
app = Flask(__name__)

@app.route('/')
def index():
    # Получаем список всех животных и передаем его в шаблон для отображения
    animals = query_db("SELECT id, name, description FROM animals")
    return render_template('index.html', animals=[{"id": row[0], "name": row[1], "description": row[2]} for row in animals])

@app.route('/animal/<int:id>')
def show_animal(id):
    # Получаем данные о конкретном животном по его ID и передаем их в шаблон
    animal_info = query_db("SELECT name, description FROM animals WHERE id=?", (id,), one=True)
    if animal_info:
        return render_template('animal.html', animal={"id": id, "name": animal_info[0], "description": animal_info[1]})
    return "Animal not found"  # Если животное не найдено, возвращаем соответствующее сообщение

@app.route('/add', methods=['GET', 'POST'])
def add_animal():
    if request.method == 'POST':  # Если запрос POST, то добавляем новое животное
        query_db("INSERT INTO animals (name, description) VALUES (?, ?)", (request.form['name'], request.form['description']))
        return redirect(url_for('index'))  # Перенаправляем на главную страницу после добавления
    return render_template('add_animal.html')  # Если запрос GET, отображаем форму для добавления животного

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_animal(id):
    if request.method == 'POST':  # Если запрос POST, то сохраняем изменения
        query_db("UPDATE animals SET name=?, description=? WHERE id=?", (request.form['name'], request.form['description'], id))
        return redirect(url_for('index'))  # Перенаправляем на главную страницу после редактирования
    animal_info = query_db("SELECT name, description FROM animals WHERE id=?", (id,), one=True)  # Получаем текущие данные о животном
    if animal_info:
        return render_template('edit_animal.html', animal={"id": id, "name": animal_info[0], "description": animal_info[1]})
    return "Animal not found"  # Если животное не найдено, возвращаем соответствующее сообщение

@app.route('/delete/<int:id>')
def delete_animal(id):
    # Удаляем животное по его ID и перенаправляем на главную страницу
    query_db("DELETE FROM animals WHERE id=?", (id,))
    return redirect(url_for('index'))

@app.route('/search', methods=['GET', 'POST'])
def search_animal():
    if request.method == 'POST':  # Если запрос POST, выполняем поиск
        search_term = '%' + request.form['search_term'] + '%'  # Формируем строку поиска
        animals = query_db("SELECT id, name, description FROM animals WHERE name LIKE ?", (search_term,))
        return render_template('search_results.html', animals=[{"id": row[0], "name": row[1], "description": row[2]} for row in animals])
    return render_template('search_animal.html')  # Если запрос GET, отображаем форму для поиска

if __name__ == "__main__":
    init_db()  # Инициализируем базу данных перед запуском приложения
    app.run(debug=True)  # Запускаем приложение в режиме отладки

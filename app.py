import sqlite3  # Импортируем библиотеку для работы с SQLite
from flask import Flask, render_template, request, redirect, url_for  # Импортируем необходимые функции и классы из Flask
from enum import Enum  # Импортируем Enum для создания перечислений

# Инициализация базы данных
db_path = "animals.db"  # Определяем путь к базе данных

def init_db():
    con = sqlite3.connect(db_path)  # Устанавливаем соединение с базой данных
    cur = con.cursor()  # Создаем курсор для выполнения SQL-запросов
    cur.execute('''CREATE TABLE IF NOT EXISTS animals
                   (id INTEGER PRIMARY KEY, name TEXT, description TEXT)''')  # Создаем таблицу, если ее еще нет
    con.commit()  # Подтверждаем изменения в базе данных
    con.close()  # Закрываем соединение с базой данных

# Enum для управления действиями
class Action(Enum):
    ADD = 'Add'  # Действие для добавления записи
    EDIT = 'Edit'  # Действие для редактирования записи
    DELETE = 'Delete'  # Действие для удаления записи
    SHOW = 'Show'  # Действие для отображения всех записей
    SEARCH = 'Search'  # Действие для поиска записи
    CLEAR = 'Clear'  # Действие для очистки данных
    EXIT = 'Exit'  # Действие для выхода из программы

# Инициализация Flask-приложения
app = Flask(__name__)  # Создаем экземпляр Flask-приложения

def get_animals():
    con = sqlite3.connect(db_path)  # Устанавливаем соединение с базой данных
    cur = con.cursor()  # Создаем курсор для выполнения SQL-запросов
    cur.execute("SELECT id, name, description FROM animals")  # Выполняем запрос для получения всех животных
    animals = [{"id": row[0], "name": row[1], "description": row[2]} for row in cur.fetchall()]  # Формируем список словарей с данными о животных
    con.close()  # Закрываем соединение с базой данных
    return animals  # Возвращаем список животных

@app.route('/')
def index():
    animals = get_animals()  # Получаем всех животных из базы данных
    return render_template('index.html', animals=animals)  # Отправляем список животных в шаблон для отображения

@app.route('/animal/<int:id>')
def show_animal(id):
    con = sqlite3.connect(db_path)  # Устанавливаем соединение с базой данных
    cur = con.cursor()  # Создаем курсор для выполнения SQL-запросов
    cur.execute("SELECT name, description FROM animals WHERE id=?", (id,))  # Выполняем запрос для получения данных о конкретном животном по id
    animal_info = cur.fetchone()  # Извлекаем данные из результата запроса
    con.close()  # Закрываем соединение с базой данных
    if animal_info:
        animal = {"id": id, "name": animal_info[0], "description": animal_info[1]}  # Формируем словарь с данными о животном
        return render_template('animal.html', animal=animal)  # Отправляем данные о животном в шаблон для отображения
    else:
        return "Animal not found", 404  # Возвращаем ошибку 404, если животное не найдено

@app.route('/add', methods=['GET', 'POST'])
def add_animal():
    if request.method == 'POST':  # Если метод запроса POST, значит пользователь отправил форму
        name = request.form['name']  # Извлекаем имя животного из формы
        description = request.form['description']  # Извлекаем описание животного из формы
        con = sqlite3.connect(db_path)  # Устанавливаем соединение с базой данных
        cur = con.cursor()  # Создаем курсор для выполнения SQL-запросов
        cur.execute("INSERT INTO animals (name, description) VALUES (?, ?)", (name, description))  # Выполняем запрос для добавления нового животного
        con.commit()  # Подтверждаем изменения в базе данных
        con.close()  # Закрываем соединение с базой данных
        return redirect(url_for('index'))  # Перенаправляем пользователя на главную страницу
    return render_template('add_animal.html')  # Если метод GET, отображаем форму для добавления животного

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_animal(id):
    if request.method == 'POST':  # Если метод запроса POST, значит пользователь отправил форму
        name = request.form['name']  # Извлекаем новое имя животного из формы
        description = request.form['description']  # Извлекаем новое описание животного из формы
        con = sqlite3.connect(db_path)  # Устанавливаем соединение с базой данных
        cur = con.cursor()  # Создаем курсор для выполнения SQL-запросов
        cur.execute("UPDATE animals SET name=?, description=? WHERE id=?", (name, description, id))  # Выполняем запрос для обновления данных о животном
        con.commit()  # Подтверждаем изменения в базе данных
        con.close()  # Закрываем соединение с базой данных
        return redirect(url_for('index'))  # Перенаправляем пользователя на главную страницу
    else:
        con = sqlite3.connect(db_path)  # Устанавливаем соединение с базой данных
        cur = con.cursor()  # Создаем курсор для выполнения SQL-запросов
        cur.execute("SELECT name, description FROM animals WHERE id=?", (id,))  # Выполняем запрос для получения текущих данных о животном
        animal_info = cur.fetchone()  # Извлекаем данные из результата запроса
        con.close()  # Закрываем соединение с базой данных
        if animal_info:
            animal = {"id": id, "name": animal_info[0], "description": animal_info[1]}  # Формируем словарь с текущими данными о животном
            return render_template('edit_animal.html', animal=animal)  # Отправляем данные в шаблон для отображения формы редактирования
        else:
            return "Animal not found", 404  # Возвращаем ошибку 404, если животное не найдено

@app.route('/delete/<int:id>')
def delete_animal(id):
    con = sqlite3.connect(db_path)  # Устанавливаем соединение с базой данных
    cur = con.cursor()  # Создаем курсор для выполнения SQL-запросов
    cur.execute("DELETE FROM animals WHERE id=?", (id,))  # Выполняем запрос для удаления животного по id
    con.commit()  # Подтверждаем изменения в базе данных
    con.close()  # Закрываем соединение с базой данных
    return redirect(url_for('index'))  # Перенаправляем пользователя на главную страницу

@app.route('/search', methods=['GET', 'POST'])
def search_animal():
    if request.method == 'POST':  # Если метод запроса POST, значит пользователь отправил форму
        search_term = request.form['search_term']  # Извлекаем поисковый запрос из формы
        con = sqlite3.connect(db_path)  # Устанавливаем соединение с базой данных
        cur = con.cursor()  # Создаем курсор для выполнения SQL-запросов
        cur.execute("SELECT id, name, description FROM animals WHERE name LIKE ?", ('%' + search_term + '%',))  # Выполняем запрос для поиска животных по имени
        animals = [{"id": row[0], "name": row[1], "description": row[2]} for row in cur.fetchall()]  # Формируем список словарей с найденными животными
        con.close()  # Закрываем соединение с базой данных
        return render_template('search_results.html', animals=animals)  # Отправляем результаты поиска в шаблон для отображения
    return render_template('search_animal.html')  # Если метод GET, отображаем форму для поиска животного

if __name__ == "__main__":
    init_db()  # Инициализируем базу данных (создаем таблицу, если ее нет)
    app.run(debug=True)  # Запускаем Flask-приложение в режиме отладки

from flask import Blueprint, url_for, redirect, abort, render_template, request, make_response, session, current_app, flash
from datetime import datetime
import psycopg2
from psycopg2.extras import RealDictCursor
import sqlite3
from os import path
from lab5 import db_connect, db_close

lab7 = Blueprint('lab7', __name__)

@lab7.context_processor
def inject_current_lab():
    return {'current_lab': '/lab7/'}

@lab7.route('/lab7/')
def main():
    return render_template("lab7/lab7.html")

@lab7.route('/lab7/rest-api/films/', methods=['GET'])
def get_films():
    try:
        conn, cur = db_connect()
        cur.execute("SELECT * FROM films")
        films = cur.fetchall()
        db_close(conn, cur)
        # Преобразование объектов Row в словари
        films = [dict(film) for film in films]
        return films
    except Exception as e:
        return {"error": str(e)}, 500

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['GET'])
def get_film(id):
    try:
        conn, cur = db_connect()
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT * FROM films WHERE id = %s", (id,))
        else:
            cur.execute("SELECT * FROM films WHERE id = ?", (id,))
        film = cur.fetchone()
        db_close(conn, cur)
        if not film:
            return {"error": "Фильм не найден"}, 404
        # Преобразование объекта Row в словарь
        return dict(film)
    except Exception as e:
        return {"error": str(e)}, 500

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['DELETE'])
def del_film(id):
    login = session.get('login')
    if not login:
        return {"error": "Пользователь не авторизован"}, 403

    try:
        conn, cur = db_connect()
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT user_id FROM films WHERE id = %s", (id,))
        else:
            cur.execute("SELECT user_id FROM films WHERE id = ?", (id,))
        film = cur.fetchone()
        if not film:
            db_close(conn, cur)
            return {"error": "Фильм не найден"}, 404

        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT id FROM users WHERE login = %s", (login,))
        else:
            cur.execute("SELECT id FROM users WHERE login = ?", (login,))
        user = cur.fetchone()
        if not user or user['id'] != film['user_id']:
            db_close(conn, cur)
            return {"error": "Пользователь не авторизован или не является автором фильма"}, 403

        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("DELETE FROM films WHERE id = %s", (id,))
        else:
            cur.execute("DELETE FROM films WHERE id = ?", (id,))
        db_close(conn, cur)
        return '', 204
    except Exception as e:
        return {"error": str(e)}, 500

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['PUT'])
def put_film(id):
    login = session.get('login')
    if not login:
        return {"error": "Пользователь не авторизован"}, 403

    try:
        conn, cur = db_connect()
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT user_id FROM films WHERE id = %s", (id,))
        else:
            cur.execute("SELECT user_id FROM films WHERE id = ?", (id,))
        film = cur.fetchone()
        if not film:
            db_close(conn, cur)
            return {"error": "Фильм не найден"}, 404

        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT id FROM users WHERE login = %s", (login,))
        else:
            cur.execute("SELECT id FROM users WHERE login = ?", (login,))
        user = cur.fetchone()
        if not user or user['id'] != film['user_id']:
            db_close(conn, cur)
            return {"error": "Пользователь не авторизован или не является автором фильма"}, 403

        film_data = request.get_json()
        current_year = datetime.now().year
        if "title" not in film_data and "title_ru" not in film_data:
            return {"title": "Заполните название или русское название"}, 400
        if "title_ru" not in film_data or film_data["title_ru"] == '':
            return {"title_ru": "Заполните русское название"}, 400
        if "title" not in film_data or film_data["title"] == '':
            film_data["title"] = film_data["title_ru"]
        if "year" not in film_data:
            return {"year": "Заполните год выпуска"}, 400
        try:
            year = int(film_data["year"])
        except ValueError:
            return {"year": "Год должен быть числом"}, 400
        if not (1895 <= year <= current_year):
            return {"year": "Год должен быть от 1895 до текущего года"}, 400
        if "description" not in film_data or film_data["description"] == '' or len(film_data["description"]) > 2000:
            return {"description": "Заполните описание (не более 2000 символов)"}, 400

        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("""
                UPDATE films SET title = %s, title_ru = %s, year = %s, description = %s, imdb = %s
                WHERE id = %s
            """, (film_data["title"], film_data["title_ru"], film_data["year"], film_data["description"], film_data.get("imdb"), id))
        else:
            cur.execute("""
                UPDATE films SET title = ?, title_ru = ?, year = ?, description = ?, imdb = ?
                WHERE id = ?
            """, (film_data["title"], film_data["title_ru"], film_data["year"], film_data["description"], film_data.get("imdb"), id))
        db_close(conn, cur)
        return film_data
    except Exception as e:
        return {"error": str(e)}, 500

@lab7.route('/lab7/rest-api/films/', methods=['POST'])
def add_film():
    login = session.get('login')
    if not login:
        return {"error": "Пользователь не авторизован"}, 403

    try:
        conn, cur = db_connect()
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT id FROM users WHERE login = %s", (login,))
        else:
            cur.execute("SELECT id FROM users WHERE login = ?", (login,))
        user = cur.fetchone()
        if not user:
            db_close(conn, cur)
            return {"error": "Пользователь не найден"}, 403

        new_film = request.get_json()
        current_year = datetime.now().year
        if "title" not in new_film and "title_ru" not in new_film:
            return {"title": "Заполните название или русское название"}, 400
        if "title_ru" not in new_film or new_film["title_ru"] == '':
            return {"title_ru": "Заполните русское название"}, 400
        if "title" not in new_film or new_film["title"] == '':
            new_film["title"] = new_film["title_ru"]
        if "year" not in new_film:
            return {"year": "Заполните год выпуска"}, 400
        try:
            year = int(new_film["year"])
        except ValueError:
            return {"year": "Год должен быть числом"}, 400
        if not (1895 <= year <= current_year):
            return {"year": "Год должен быть от 1895 до текущего года"}, 400
        if "description" not in new_film or new_film["description"] == '' or len(new_film["description"]) > 2000:
            return {"description": "Заполните описание (не более 2000 символов)"}, 400

        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("""
                INSERT INTO films (user_id, title, title_ru, year, description, imdb)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id
            """, (user['id'], new_film["title"], new_film["title_ru"], new_film["year"], new_film["description"], new_film.get("imdb")))
            new_id = cur.fetchone()['id']
        else:
            cur.execute("""
                INSERT INTO films (user_id, title, title_ru, year, description, imdb)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (user['id'], new_film["title"], new_film["title_ru"], new_film["year"], new_film["description"], new_film.get("imdb")))
            new_id = cur.lastrowid
        db_close(conn, cur)
        return {'id': new_id}, 201
    except Exception as e:
        return {"error": str(e)}, 500

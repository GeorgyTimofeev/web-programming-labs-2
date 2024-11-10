from os import close
from flask import Blueprint, url_for, redirect, abort, render_template, request, make_response, session, current_app
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from os import path

lab5 = Blueprint('lab5',__name__)

@lab5.context_processor
def inject_current_lab():
    return {'current_lab': '/lab5/'}

def db_connect():
    if current_app.config['DB_TYPE'] == 'postgres':
        conn = psycopg2.connect(
            host='127.0.0.1',
            database='georgy_timofeev_knowledge_base',
            user='georgy_timofeev_knowledge_base',
            password='web_password'
        )
        cur = conn.cursor(cursor_factory=RealDictCursor)
    else:
        dir_path = path.dirname(path.realpath(__file__))
        db_path = path.join(dir_path, 'database.db')
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

    return conn, cur

def db_close(conn, cur):
    if conn and cur:
        conn.commit()
        cur.close()
        conn.close()

@lab5.route('/lab5/')
def lab():
    return render_template('lab5/lab5.html', login=session.get('login'))

@lab5.route('/lab5/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab5/register.html')

    login = request.form.get('login')
    password = request.form.get('password')

    if not (login and password):
        return render_template('lab5/register.html', error='Заполните все поля')

    conn, cur = db_connect()
    if not conn or not cur:
        return render_template('lab5/register.html', error='Ошибка подключения к базе данных')

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT login FROM users WHERE login = %s;", (login, ))
    else:
        cur.execute("SELECT login FROM users WHERE login = ?;", (login, ))

    if cur.fetchone():
        db_close(conn, cur)
        return render_template('lab5/register.html', error='Пользователь с таким логином уже существует')

    password_hash = generate_password_hash(password)

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("INSERT INTO users (login, password) VALUES (%s, %s);", (login, password_hash))
    else:
        cur.execute("INSERT INTO users (login, password) VALUES (?, ?);", (login, password_hash))

    db_close(conn, cur)

    return render_template('lab5/succes.html', login=login)

@lab5.route('/lab5/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab5/login.html')

    login = request.form.get('login')
    password = request.form.get('password')

    if not (login and password):
        return render_template('lab5/login.html', error='Заполните все поля')

    conn, cur = db_connect()
    if not conn or not cur:
        return render_template('lab5/login.html', error='Ошибка подключения к базе данных')

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM users WHERE login = %s;", (login, ))
    else:
        cur.execute("SELECT * FROM users WHERE login = ?;", (login, ))

    user = cur.fetchone()

    if not user:
        db_close(conn, cur)
        return render_template('lab5/login.html', error='Пользователь не найден')

    if not check_password_hash(user['password'], password):
        db_close(conn, cur)
        return render_template('lab5/login.html', error='Неверный пароль')

    session['login'] = login

    db_close(conn, cur)
    return render_template('lab5/succes_login.html', login=login)

@lab5.route('/lab5/logout/', methods=['GET','POST'])
def logout():
    session.pop('login', None)
    session.pop('name', None)
    return redirect(url_for('lab5.login'))

@lab5.route('/lab5/create/', methods=['GET', 'POST'])
def create():
    login = session.get('login')
    if not login:
        return redirect(url_for('lab5.login'))

    if request.method == 'GET':
        return render_template('lab5/create_article.html')

    title = request.form.get('title')
    article_text = request.form.get('article_text')

    if not (title and article_text):
        return render_template('lab5/create_article.html', error='Заполните все поля')

    conn, cur = db_connect()
    if not conn or not cur:
        return render_template('lab5/create_article.html', error='Ошибка подключения к базе данных')

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT id FROM users WHERE login=%s;", (login, ))
    else:
        cur.execute("SELECT id FROM users WHERE login=?;", (login, ))

    user_id = cur.fetchone()
    if not user_id:
        db_close(conn, cur)
        return render_template('lab5/create_article.html', error='Пользователь не найден')

    user_id = user_id["id"]

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("INSERT INTO articles (user_id, title, article_text) VALUES (%s, %s, %s)", (user_id, title, article_text))
    else:
        cur.execute("INSERT INTO articles (login_id, title, article_text) VALUES (?, ?, ?)", (user_id, title, article_text))

    db_close(conn, cur)
    return redirect(url_for('lab5.lab'))

@lab5.route('/lab5/list/')
def list():
    login = session.get('login')
    if not login:
        return redirect(url_for('lab5.login'))

    conn, cur = db_connect()
    if not conn or not cur:
        return render_template('lab5/articles.html', error='Ошибка подключения к базе данных')

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT id FROM users WHERE login=%s;", (login, ))
    else:
        cur.execute("SELECT id FROM users WHERE login=?;", (login, ))

    login_id = cur.fetchone()
    if not login_id:
        db_close(conn, cur)
        return render_template('lab5/articles.html', error='Пользователь не найден')

    login_id = login_id["id"]

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM articles WHERE user_id=%s;", (login_id, ))
    else:
        cur.execute("SELECT * FROM articles WHERE login_id=?;", (login_id, ))

    articles = cur.fetchall()

    db_close(conn, cur)

    if not articles:
        return render_template('lab5/articles.html', message='У вас нет ни одной статьи')

    return render_template('lab5/articles.html', articles=articles)

@lab5.route('/lab5/edit/<int:article_id>/', methods=['GET', 'POST'])
def edit(article_id):
    login = session.get('login')
    if not login:
        return redirect(url_for('lab5.login'))

    conn, cur = db_connect()
    if not conn or not cur:
        return render_template('lab5/create_article.html', error='Ошибка подключения к базе данных')

    if request.method == 'GET':
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT * FROM articles WHERE id=%s AND user_id=(SELECT id FROM users WHERE login=%s);", (article_id, login))
        else:
            cur.execute("SELECT * FROM articles WHERE id=? AND login_id=(SELECT id FROM users WHERE login=?);", (article_id, login))

        article = cur.fetchone()
        db_close(conn, cur)

        if not article:
            return render_template('lab5/create_article.html', error='Статья не найдена')

        return render_template('lab5/create_article.html', article=article)

    title = request.form.get('title')
    article_text = request.form.get('article_text')

    if not (title and article_text):
        return render_template('lab5/create_article.html', error='Заполните все поля', article={'id': article_id, 'title': title, 'article_text': article_text})

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("UPDATE articles SET title=%s, article_text=%s WHERE id=%s AND user_id=(SELECT id FROM users WHERE login=%s);", (title, article_text, article_id, login))
    else:
        cur.execute("UPDATE articles SET title=?, article_text=? WHERE id=? AND login_id=(SELECT id FROM users WHERE login=?);", (title, article_text, article_id, login))

    db_close(conn, cur)
    return redirect(url_for('lab5.list'))

@lab5.route('/lab5/delete/<int:article_id>/', methods=['POST'])
def delete(article_id):
    login = session.get('login')
    if not login:
        return redirect(url_for('lab5.login'))

    conn, cur = db_connect()
    if not conn or not cur:
        return render_template('lab5/articles.html', error='Ошибка подключения к базе данных')

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("DELETE FROM articles WHERE id=%s AND user_id=(SELECT id FROM users WHERE login=%s);", (article_id, login))
    else:
        cur.execute("DELETE FROM articles WHERE id=? AND login_id=(SELECT id FROM users WHERE login=?);", (article_id, login))

    db_close(conn, cur)
    return redirect(url_for('lab5.list'))

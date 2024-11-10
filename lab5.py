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
    is_public = request.form.get('is_public') == 'on'

    if not (title and article_text):
        return render_template('lab5/create_article.html', error='Заполните все поля')

    conn, cur = db_connect()
    if not conn or not cur:
        return render_template('lab5/create_article.html', error='Ошибка подключения к базе данных')

    # Сначала получаем user_id
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT id FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT id FROM users WHERE login=?;", (login,))

    user = cur.fetchone()
    if not user:
        db_close(conn, cur)
        return render_template('lab5/create_article.html', error='Пользователь не найден')

    user_id = user['id']

    # Затем используем полученный user_id для создания статьи
    try:
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("""
                INSERT INTO articles (user_id, title, article_text, is_public, is_favorite, likes)
                VALUES (%s, %s, %s, %s, %s, %s)
                """, (user_id, title, article_text, is_public, False, 0))
        else:
            cur.execute("""
                INSERT INTO articles (login_id, title, article_text, is_public, is_favorite, likes)
                VALUES (?, ?, ?, ?, ?, ?)
                """, (user_id, title, article_text, is_public, False, 0))

        conn.commit()
        db_close(conn, cur)
        return redirect(url_for('lab5.lab'))

    except Exception as e:
        db_close(conn, cur)
        return render_template('lab5/create_article.html', error=f'Ошибка при создании статьи: {str(e)}')


@lab5.route('/lab5/list/')
def list():
    login = session.get('login')

    conn, cur = db_connect()
    if not conn or not cur:
        return render_template('lab5/articles.html', error='Ошибка подключения к базе данных')

    user_id = None
    if login:
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT id FROM users WHERE login=%s;", (login,))
        else:
            cur.execute("SELECT id FROM users WHERE login=?;", (login,))
        user = cur.fetchone()
        user_id = user['id'] if user else None

    # Разные запросы для PostgreSQL и SQLite
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("""
            SELECT a.*,
                   (SELECT COUNT(*) FROM favorites WHERE article_id=a.id) as star_count,
                   EXISTS(SELECT 1 FROM favorites WHERE article_id=a.id AND user_id=%s) as is_favorited
            FROM articles a
            WHERE is_public=True
            ORDER BY is_favorited DESC, likes DESC;
        """, (user_id,))
    else:
        cur.execute("""
            SELECT a.*,
                   (SELECT COUNT(*) FROM favorites WHERE article_id=a.id) as star_count,
                   EXISTS(SELECT 1 FROM favorites WHERE article_id=a.id AND user_id=?) as is_favorited
            FROM articles a
            WHERE is_public=1
            ORDER BY is_favorited DESC, likes DESC;
        """, (user_id,))

    articles = cur.fetchall()

    # Получаем логины пользователей
    user_logins = {}
    for article in articles:
        # Используем правильное имя столбца в зависимости от типа БД
        article_user_id = article['user_id'] if current_app.config['DB_TYPE'] == 'postgres' else article['login_id']

        if article_user_id not in user_logins:
            if current_app.config['DB_TYPE'] == 'postgres':
                cur.execute("SELECT login FROM users WHERE id=%s;", (article_user_id,))
            else:
                cur.execute("SELECT login FROM users WHERE id=?;", (article_user_id,))
            user_login = cur.fetchone()
            if user_login:
                user_logins[article_user_id] = user_login['login']

    db_close(conn, cur)

    if not articles:
        return render_template('lab5/articles.html', message='Нет публичных статей', page_title='Публичные статьи')

    return render_template('lab5/articles.html',
                         articles=articles,
                         user_logins=user_logins,
                         login_id=user_id,
                         page_title='Публичные статьи',
                         is_postgres=(current_app.config['DB_TYPE'] == 'postgres'))

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
    is_public = request.form.get('is_public') == 'on'

    if not (title and article_text):
        return render_template('lab5/create_article.html', error='Заполните все поля', article={'id': article_id, 'title': title, 'article_text': article_text, 'is_public': is_public})

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("UPDATE articles SET title=%s, article_text=%s, is_public=%s WHERE id=%s AND user_id=(SELECT id FROM users WHERE login=%s);", (title, article_text, is_public, article_id, login))
    else:
        cur.execute("UPDATE articles SET title=?, article_text=?, is_public=? WHERE id=? AND login_id=(SELECT id FROM users WHERE login=?);", (title, article_text, is_public, article_id, login))

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

@lab5.route('/lab5/users/')
def users():
    login = session.get('login')
    if not login:
        return redirect(url_for('lab5.login'))

    conn, cur = db_connect()
    if not conn or not cur:
        return render_template('lab5/users.html', error='Ошибка подключения к базе данных')

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT login FROM users;")
    else:
        cur.execute("SELECT login FROM users;")

    users = cur.fetchall()

    db_close(conn, cur)

    if not users:
        return render_template('lab5/users.html', message='Нет зарегистрированных пользователей')

    return render_template('lab5/users.html', users=users)

@lab5.route('/lab5/favorite/<int:article_id>/', methods=['POST'])
def favorite(article_id):
    login = session.get('login')
    if not login:
        return redirect(url_for('lab5.login'))

    conn, cur = db_connect()
    if not conn or not cur:
        return redirect(url_for('lab5.list'))

    # Получаем ID пользователя
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT id FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT id FROM users WHERE login=?;", (login,))

    user = cur.fetchone()
    user_id = user['id']

    # Проверяем, есть ли уже статья в избранном
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT id FROM favorites WHERE user_id=%s AND article_id=%s;",
                   (user_id, article_id))
    else:
        cur.execute("SELECT id FROM favorites WHERE user_id=? AND article_id=?;",
                   (user_id, article_id))

    favorite = cur.fetchone()

    if favorite:
        # Удаляем из избранного
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("DELETE FROM favorites WHERE user_id=%s AND article_id=%s;",
                       (user_id, article_id))
            cur.execute("UPDATE articles SET likes = likes - 1 WHERE id=%s;",
                       (article_id,))
        else:
            cur.execute("DELETE FROM favorites WHERE user_id=? AND article_id=?;",
                       (user_id, article_id))
            cur.execute("UPDATE articles SET likes = likes - 1 WHERE id=?;",
                       (article_id,))
    else:
        # Добавляем в избранное
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("INSERT INTO favorites (user_id, article_id) VALUES (%s, %s);",
                       (user_id, article_id))
            cur.execute("UPDATE articles SET likes = likes + 1 WHERE id=%s;",
                       (article_id,))
        else:
            cur.execute("INSERT INTO favorites (user_id, article_id) VALUES (?, ?);",
                       (user_id, article_id))
            cur.execute("UPDATE articles SET likes = likes + 1 WHERE id=?;",
                       (article_id,))

    db_close(conn, cur)
    return redirect(url_for('lab5.list'))

@lab5.route('/lab5/user_articles/')
def user_articles():
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
        cur.execute("SELECT * FROM articles WHERE user_id=%s;", (login_id,))
    else:
        cur.execute("SELECT * FROM articles WHERE login_id=?;", (login_id,))

    articles = cur.fetchall()

    # Получаем логины пользователей
    user_logins = {}
    for article in articles:
        user_id = article['user_id']
        if user_id not in user_logins:
            if current_app.config['DB_TYPE'] == 'postgres':
                cur.execute("SELECT login FROM users WHERE id=%s;", (user_id,))
            else:
                cur.execute("SELECT login FROM users WHERE id=?;", (user_id,))
            user_login = cur.fetchone()
            if user_login:
                user_logins[user_id] = user_login['login']

    db_close(conn, cur)

    if not articles:
        return render_template('lab5/articles.html', message='У вас нет ни одной статьи', page_title='Мои статьи')

    return render_template('lab5/articles.html', articles=articles, user_logins=user_logins, login_id=login_id, page_title='Мои статьи')

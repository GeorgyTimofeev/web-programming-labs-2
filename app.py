from flask import Flask, url_for, redirect

app = Flask(__name__)

@app.errorhandler(404)
def not_found(err):
    return "Такой страницы не существует", 404

@app.route('/lab1/web')
def web():
    return '''<!doctype html>
        <html>
           <head>
                <link rel="stylesheet" type="text/css" href="''' + url_for('static', filename='lab1.css') + '''">
            </head>
           <body>
               <h1>web-сервер на flask</h1>
                <a href="/lab1/author">Автор</a>
           </body>
        </html>''', 200, {
            'X-Server': 'sample',
            'Content-Type': 'text/plain; charset=utf-8'
        }

@app.route('/lab1/author')
def author():
    name = "Тимофеев Георгий Алексеевич"
    group = "ФБИ-22"
    faculty = "ФБ"

    return '''<!doctype html>
        <html>
            <head>
                <link rel="stylesheet" type="text/css" href="''' + url_for('static', filename='lab1.css') + '''">
            </head>
            <body>
                <p>Студент: ''' + name + '''</p>
                <p>Группа: ''' + group + '''</p>
                <p>Факультет: ''' + faculty + '''</p>
                <a href="/lab1/web">На страницу "web"</a>
            </body>
        </html>'''

@app.route('/lab1/oak')
def oak():
    path = url_for('static', filename='oak.jpg')
    style = url_for('static', filename='lab1.css')
    return '''
<!doctype html>
<html>
    <head>
        <link rel="stylesheet" type="text/css" href="''' + style + '''">
    </head>
    <body>
        <h1>Дуб</h1>
        <img src="''' + path + '''">
    </body>
</html>
'''

count = 0
@app.route('/lab1/counter')
def counter():
    global count
    count += 1
    return '''
<!doctype html>
<html>
    <head>
        <link rel="stylesheet" type="text/css" href="''' + url_for('static', filename='lab1.css') + '''">
    </head>
    <body>
        <h1>Счётчик</h1>
        <p>Сколько раз вы заходили на эту страницу: ''' + str(count) + '''</p>
        <a href="/lab1/counter_cleaner">Обнулить счётчик</a>
    </body>
</html>
'''

@app.route('/lab1/counter_cleaner')
def counter_cleaner():
    global count
    count = 0
    return redirect('/lab1/counter')

@app.route('/lab1/info')
def info():
    return redirect('/lab1/author')

@app.route('/lab1/created')
def created():
    return '''
<!doctype html>
<html>
    <head>
        <link rel="stylesheet" type="text/css" href="''' + url_for('static', filename='lab1.css') + '''">
    </head>
    <body>
        <h1>Создано успешно</h1>
        <div><i>что-то создано…</i></div>
    </body>
</html>
''', 201

from flask import Flask, url_for, redirect
from werkzeug.exceptions import HTTPException

app = Flask(__name__)

@app.errorhandler(400)
def bad_request(err):
    return '''Неверный запрос. Сервер не может или не будет обрабатывать запрос из-за чего-то,
    что воспринимается как ошибка клиента (например, неправильный синтаксис, формат
    или маршрутизация запроса).''', 400

@app.errorhandler(401)
def unauthorized(err):
    return '''Для доступа к ресурсу требуется аутентификация.
    Клиент должен передать заголовок Authorization в запросе.''', 401

class PaymentRequired(HTTPException):
    code = 402
    description = 'Payment Required'

@app.errorhandler(PaymentRequired)
def payment_required(err):
    return '''Зарезервировано для будущего использования.
    Используется для целей тестирования оплаты.''', 402

@app.errorhandler(403)
def forbidden(err):
    return '''Клиент не имеет прав доступа к содержимому,
    поэтому сервер отказывает в выполнении запроса.''', 403

@app.errorhandler(404)
def not_found(err):
    return '''
<!doctype html>
<html>
    <head>
        <link rel="stylesheet" type="text/css" href="''' + url_for('static', filename='lab1.css') + '''">
        <tytle>Ошибка 404</tytle>
    </head>
    <body>
        <h1>Упс… Кажется такой страницы не существует</h1>
        <p>Сервер не может найти запрошенный ресурс. В браузере это означает,
        что URL-адрес не распознан. В API это также может означать,
        что адрес правильный, но ресурс не существует.</p>

        <img src="''' + url_for('static', filename='Error_404_img.png') + '''" style="width: 300px;
        position: absolute; top: 60%; right: 50px; transform: translateY(-50%);"></br>

        <a href="/">Вернуться на главную</a>
    </body>
''', 404

@app.errorhandler(405)
def method_not_allowed(err):
    return '''Метод, указанный в запросе (например, POST, PUT, DELETE) не применим к ресурсу,
    и сервер не поддерживает его.''', 405

@app.errorhandler(418)
def i_am_a_teapot(err):
    return '''Определенный в RFC 2324. Этот код составляет часть
    апрельской шутки и не должен использоваться для серьезных целей.''', 418

@app.errorhandler(500)
def internal_server_error(err):
    return '''
<!doctype html>
<html>
    <head>
        <link rel="stylesheet" type="text/css" href="''' + url_for('static', filename='lab1.css') + '''">
        <tytle>Ошибка 500</tytle>
    </head>
    <body>
        <h1>Внутренняя ошибка сервера</h1>
        <p>На сервере произошла ошибка, в результате которой он не может успешно обработать запрос.
        Пожалуйста, попробуйте позже.</p>

        <img src="''' + url_for('static', filename='Error_500_img.png') + '''" style="width: 300px;
        position: absolute; top: 50%; right: 100px; transform: translateY(-50%);"></br>
        <a href="/">Вернуться на главную</a>
    </body>
</html>
''', 500

@app.route('/lab1/an_error')
def make_an_error():
    return 1 / 0

@app.route('/')
@app.route('/index')
def index():
    return '''
<!doctype html>
<html>
    <head>
        <tytle>НГТУ, ФБ, Лабораторные работы</tytle>
        <link rel="stylesheet" type="text/css" href="''' + url_for('static', filename='lab1.css') + '''">
    </head>
    <body>
        <header>НГТУ, ФБ, WEB-программирование, часть 2. Список лабораторных</header>
        <ol>
            <li><a href="/lab1">Первая Лабораторная</a></li>
        </ol>
    </body>
    <footer>
        Тимофеев Георгий Алексеевич, ФБИ-22, 3 Курс, 2024 год.
    </footer>
</html>
'''

@app.route('/lab1')
def lab1():
    return'''
<!doctype html>
<html>
    <head>
        <tytle>Лабораторная 1</tytle>
        <link rel="stylesheet" type="text/css" href="''' + url_for('static', filename='lab1.css') + '''">
    </head>
    <body>
        <h1>Flask</h1>
        <p>Flask — фреймворк для создания веб-приложений на языке программирования Python,
        использующий набор инструментов Werkzeug, а также шаблонизатор Jinja2. Относится
        к категории так называемых микрофреймворков — минималистичных каркасов веб-приложений,
        сознательно предоставляющих лишь самые базовые возможности.</p>

        <a href="/">Назад на главную</a></li>

        <h2>Список rout'ов:</h2>
        <ol>
            <li><a href="/index">/index</a></li>
            <li><a href="/lab1">/lab1</a></li>
            <li><a href="/lab1/web">/lab1/web</a></li>
            <li><a href="/lab1/info">/lab1/info</a></li>
            <li><a href="/lab1/author">/lab1/author</a></li>
            <li><a href="/lab1/oak">/lab1/oak</a></li>
            <li><a href="/lab1/counter">/lab1/counter</a></li>
            <li><a href="/lab1/counter_cleaner">/lab1/counter_cleaner</a></li>
            <li><a href="/lab1/an_error">/lab1/an_error</a></li>
            <li><a href="/lab1/created">/lab1/created</a></li>
            <li><a href="/lab1/new_route">/lab1/new_route</a></li>
        </ol>
    </body>
    <footer>
        Тимофеев Георгий Алексеевич, ФБИ-22, 3 Курс, 2024 год.
    </footer>
</html>
'''

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

@app.route('/lab1/new_route')
def new_route():
    return '''
<!doctype html>
<html>
    <head>
        <link rel="stylesheet" type="text/css" href="''' + url_for('static', filename='lab1.css') + '''">
        <tytle>Sigmaringen Castle</tytle>
    </head>
    <body>
        <p>From Wikipedia, the free encyclopedia</p>
        <div class="text_container" style='width: 50%'>
            <p style='margin-top: 10px'><b>Sigmaringen Castle</b> (German: Schloss Sigmaringen) was the princely castle and seat
            of government for the Princes of Hohenzollern-Sigmaringen. Situated in the Swabian Alb region
            of Baden-Württemberg, Germany, this castle dominates the skyline of the town of Sigmaringen.
            The castle was rebuilt following a fire in 1893, and only the towers of the earlier medieval
            fortress remain. Schloss Sigmaringen was a family estate of the Swabian Hohenzollern family,
            a cadet branch of the Hohenzollern family, from which the German Emperors and kings of
            Prussia came. During the closing months of World War II, Schloss Sigmaringen was briefly
            the seat of the Vichy French Government after France was liberated by the Allies.
            The castle and museums may be visited throughout the year, but only on guided tours.
            It is still owned by the Hohenzollern-Sigmaringen family, although they
            no longer reside there.</p>

            <h1>Location</h1>
            <p>Sigmaringen is located on the southern edge of the Swabian Jura,
            a plateau region in southern Baden-Württemberg. The Hohenzollern
            castle was built below the narrow Danube river valley in the modern
            Upper Danube Nature Park (German: Naturpark Obere Donau). The castle
            rises above the Danube on a towering chalk projection that is a spur of
            the white Jura Mountains formation. The hill is known simply as the
            Schlossberg or Castle Rock. The Schlossberg is about 200 meters (660 ft)
            long and up to 35 meters (115 ft) above the river. On this free-standing
            towering rock, the princely Hohenzollern castle is the largest of the Danube
            valley castles. The sheer cliffs and steep sides of the tower made it a
            natural site for a well-protected medieval castle.</p>

            <a href="/lab1">Назад на страницу лабораторной</a>
        </div>

        <div class="image_container" style='position: absolute; right: 50px; top: 10%'>
            <img src="''' + url_for('static', filename='Sigmaringen_Castle.jpeg') + '''"></br>
            <img src="''' + url_for('static', filename='Sigmaringen_Castle_2.jpeg') + '''" style='margin-top: 10px'>
        </div>
    </body>
    <footer>Тимофеев Георгий Алексеевич, ФБИ-22, 3 Курс, 2024 год.</footer>
</html>
''', 200, {
    'Content-Language': 'en',
    'X-Nerd': '42',
    'X-Student': 'Timofeev Georgy'
}

from flask import Flask

app = Flask(__name__)

@app.route('/web')
def web():
    return '''<!doctype html>
        <html>
           <body>
               <h1>web-сервер на flask</h1>
                <a href="/author">Автор</a>
           </body>
        </html>'''

@app.route('/author')
def author():
    name = "Тимофеев Георгий Алексеевич"
    group = "ФБИ-22"
    faculty = "ФБ"

    return '''<!doctype html>
        <html>
            <body>
                <p>Студент: ''' + name + '''</p>
                <p>Группа: ''' + group + '''</p>
                <p>Факультет: ''' + faculty + '''</p>
                <a href="/web">На страницу "web"</a>
            </body>
        </html>'''

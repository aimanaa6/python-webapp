from flask import render_template, session, request
import random
from application import app
from application.data_access import DataAccess

@app.route('/')
@app.route('/home')
def home():
    session['loggedIn'] = False
    return render_template('home.html', title='Home')


@app.route('/welcome/<string:name>')
def welcome(name='Team'):
    return render_template('welcome.html', title="Welcome", name=name.title(), group='Everyone')


@app.route('/joke')
def joke():
    db = DataAccess()
    jokes = db.query("SELECT * from joke;")
    joke_number = random.randrange(len(jokes))
    joke_question = jokes[joke_number][1]
    joke_answer = jokes[joke_number][2]
    return render_template('joke.html', title="Joke Time", joke_question=joke_question, joke_answer=joke_answer, number_of_jokes=len(jokes))


@app.route('/hello')
def hello():
    return render_template('hello.html', title='Hello')

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('username')
        try:
            db = DataAccess()
            query = f"INSERT into users(username) values ('{name}')"
            db.execute(query)
        except Exception as error:
            print(error)
    return render_template('register.html')

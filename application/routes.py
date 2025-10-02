import random

from flask import render_template, session, request, jsonify, url_for, redirect, make_response

from application import app
from application.data_access import DataAccess
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title='Home')


@app.route('/welcome/<string:name>')
def welcome(name='Team'):
    token = request.cookies.get('jwt_token')
    if not token:
        return make_response(redirect(url_for('login')))
    return render_template('welcome.html', title="Welcome", name=name.title(), group='Everyone')


@app.route('/joke')
def joke():
    token = request.cookies.get('jwt_token')
    if not token:
        return make_response(redirect(url_for('login')))

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
        hashed_password = generate_password_hash(request.form.get('password'))
        try:
            db = DataAccess()
            query = f"CALL add_user('{name}', '{hashed_password}')"
            db.execute(query)

            return redirect(url_for('login'))
        except Exception as error:
            print(error)
            return render_template('register.html', title='Register', error=error)
    return render_template('register.html', title='Register')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        name = request.form.get('username')
        password = request.form.get('password')
        try:
            db = DataAccess()
            query = f"select id, hashed_password from users where username = '{name}'"
            user_id, db_hashed_password = db.query(query)[0]
            if not db_hashed_password or not check_password_hash(db_hashed_password, password):
                return render_template('login.html', title='Login', error='Invalid email or password', )

            access_token = create_access_token(identity=str(user_id))
            response = make_response(redirect(url_for('joke')))
            response.set_cookie('jwt_token', access_token)
            return response
        except Exception as error:
            print(error)
            return render_template('login.html', title='Login', error=error)
    return render_template('login.html')

@app.route('/logout')
def logout():
    response = make_response(redirect(url_for('login')))
    response.delete_cookie('jwt_token')
    return response

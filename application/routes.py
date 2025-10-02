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
    # token remains active in joke page
    token = request.cookies.get('jwt_token')
    # if there is no token user gets redirected to login page
    if not token:
        return make_response(redirect(url_for('login')))

    db = DataAccess()
    # class DataAccess executes SQL query
    jokes = db.query("SELECT * from joke;")
    joke_number = random.randrange(len(jokes))
    joke_question = jokes[joke_number][1]
    joke_answer = jokes[joke_number][2]
    # parameters passed through render template generate jokes from database
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
        # post method data is being updated - get only retrieves the form
        # grabbing username and password
        name = request.form.get('username')
        password = request.form.get('password')
        try:
            # data access class connects to my SQL
            db = DataAccess()
            query = f"select id, hashed_password from users where username = '{name}'"
            # fetch username and password and takes the first result row
            user_id, db_hashed_password = db.query(query)[0]
            if not db_hashed_password or not check_password_hash(db_hashed_password, password):
                return render_template('login.html', title='Login', error='Invalid email or password', )
            # compares the entered password with stored hash password
            # if there is no match returns a JSON error with 401 error
            # successful login - session is active in Flask
            access_token = create_access_token(identity=str(user_id))
            # access token is generated (JWT) AND redirected to joke page (can't be accessed without user session being active)
            response = make_response(redirect(url_for('joke')))
            # JWT token is set in browser cookie
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


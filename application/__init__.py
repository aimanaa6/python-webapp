from flask import Flask
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config['SECRET_KEY'] = '4c623e5aca307230468a2fc37c380f8d'
jwt = JWTManager(app)

from application import routes



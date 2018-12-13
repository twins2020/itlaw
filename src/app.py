from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from src.security import authenticate, identity
from src.resources.user import UserRegister
from src.resources.dosar import Dosar, DosarList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'jose'
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


jwt = JWT(app, authenticate, identity)  # /auth

api.add_resource(Dosar, '/dosar')
api.add_resource(DosarList, '/dosare')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    from src.db import db

    db.init_app(app)
    app.run(port=5000, debug=True)

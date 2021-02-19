from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tv.db'
db = SQLAlchemy(app)


class TV(db.Model):
    name = db.Column(db.String(50), unique=True, nullable=False)
    monthly_price = db.Column(db.Integer)


class Channel(db.Model):
    name = db.Column(db.String(50), unique=True, nullable=False)


    @app.route('/')
    def hello_world():
        return 'Hello World!'

    if __name__ == '__main__':
        app.run()

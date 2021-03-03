from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tv.db'
app.config['SQLAlCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

relations = db.Table('relations',
                     db.Column('tv_id', db.Integer, db.ForeignKey('TV.tv_id')),
                     db.Column('channel_id', db.Integer, db.ForeignKey('channel.channel_id'))
                     )


class Channel(db.Model):
    channel_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)


class TV(db.Model):
    tv_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    monthly_price = db.Column(db.Integer)
    channels = db.relationship('Channel', secondary=relations, backref='tvs')


@app.route('/')
def index():
    tvs = TV.query.all()
    channels = Channel.query.all()
    return render_template("index.html", tvs=tvs, channels=channels)


@app.route('/channels')
def channels():
    channels = Channel.query.all()
    return render_template("channels.html", channels=channels)


if __name__ == '__main__':
    app.run()

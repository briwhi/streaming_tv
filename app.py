from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from forms import ChannelForm, TVForm

app = Flask(__name__)

app.secret_key = "Secret Key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tv.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

relations = db.Table('relations',
                     db.Column('tv_id', db.Integer, db.ForeignKey('TV.tv_id')),
                     db.Column('channel_id', db.Integer, db.ForeignKey('channel.channel_id'))
                     )


class Channel(db.Model):
    channel_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    short_name = db.Column(db.String(10), unique=True)


class TV(db.Model):
    tv_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    monthly_price = db.Column(db.Float)
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


@app.route('/service/add', methods=['GET', 'POST'])
def add_service():
    tv = TV()
    form = TVForm(obj=tv)
    if form.validate_on_submit():
        form.populate_obj(tv)
        db.session.add(tv)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template("edit_service.html", form=form)
    


@app.route('/channel/add', methods=['GET', 'POST'])
def add_channel():
    channel = Channel()
    form = ChannelForm(obj=channel)
    if form.validate_on_submit():
        form.populate_obj(channel)
        db.session.add(channel)
        db.session.commit()
        return redirect(url_for('channels'))
    return render_template("edit_channel.html", form=form)


if __name__ == '__main__':
    app.run()

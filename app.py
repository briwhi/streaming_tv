from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from forms import ChannelForm, TVForm, IndexForm

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


@app.route('/', methods=['GET', 'POST'])
def index():
    tvs = TV.query.all()
    channels = Channel.query.all()
    s_channels = []
    form = IndexForm()
    if form.validate_on_submit():
        print("valid")
    else:
        print("invalid")
    return render_template("index.html", tvs=tvs, channels=channels, s_channels=s_channels, form=form)


@app.route('/channels')
def channels():
    channels = Channel.query.all()
    return render_template("channels.html", channels=channels)


@app.route('/service/add', methods=['GET', 'POST'])
def service_add():
    tv = TV()
    channels = Channel.query.order_by(Channel.name).all()
    form = TVForm(obj=tv)
    if form.validate_on_submit():
        form.populate_obj(tv)
        db.session.add(tv)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template("edit_service.html", form=form, channels=channels)


@app.route('/service/edit/<tv_id>', methods=['GET', 'POST'])
def service_edit(tv_id):
    tv = TV.query.get(tv_id)
    channels = Channel.query.order_by(Channel.name).all()
    form = TVForm(obj=tv)
    if form.validate_on_submit():
        form.populate_obj(tv)
        for channel in channels:
            if channel.short_name in request.form:
                add_channel_to_service(tv, channel)
            else:
                remove_channel_from_service(tv, channel)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template("edit_service.html", form=form, tv = tv, channels=channels)


@app.route('/channel/add', methods=['GET', 'POST'])
def channel_add():
    channel = Channel()
    form = ChannelForm(obj=channel)
    if form.validate_on_submit():
        form.populate_obj(channel)
        db.session.add(channel)
        db.session.commit()
        return redirect(url_for('channels'))
    return render_template("edit_channel.html", form=form)


@app.route('/channel/edit/<channel_id>', methods=['GET', 'POST'])
def channel_edit(channel_id):
    channel = Channel.query.get(channel_id)
    form = ChannelForm(obj=channel)
    
    return render_template("edit_channel.html", form=form, channel=channel)






def add_channel_to_service(tv, channel):
    if channel in tv.channels:
        return
    else:
        tv.channels.append(channel)



def remove_channel_from_service(tv, channel):
    if channel in tv.channels:
        tv.channels.remove(channel)
    else:
        return




if __name__ == '__main__':
    app.run()

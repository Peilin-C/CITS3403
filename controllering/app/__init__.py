from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from app.config import Config

from flask import render_template, flash, redirect


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes, models

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/browse_users.html')
def browse_users():
    return render_template('browse_users.html')

@app.route('/create_session.html')
def create_session():
    return render_template('create_session.html')

@app.route('/study_sessions.html')
def study_sessions():
    return render_template('study_sessions.html')

@app.route('/login.html')
def login():
    return render_template('login.html')

@app.route('/edit_profile.html')
def edit_profile():
    return render_template('edit_profile.html')

@app.route('/profile.html')
def profile():
    return render_template('profile.html')


###
#@app.route('/login', methods=['GET', 'POST'])
#def login():
#    form = LoginForm()
#    if form.validate_on_submit():
#        flash('Login requested for user {}, remember_me={}'.format(
#            form.username.data, form.remember_me.data))
#        return redirect('/index')
#    return render_template('login.html', title='Sign In', form=form)

###

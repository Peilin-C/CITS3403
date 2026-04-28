from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models import User
from app import db

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('index.html')

@main.route('/browse')
@login_required
def browse():
    unit = request.args.get('unit', '')
    availability = request.args.get('availability', '')
    study_style = request.args.get('study_style', '')
    users = User.query.filter(User.id != current_user.id)
    if unit:
        users = users.filter(User.units.contains(unit))
    if availability:
        users = users.filter(User.availability.contains(availability))
    if study_style:
        users = users.filter(User.study_style.contains(study_style))
    users = users.all()
    return render_template('browse_users.html', users=users)

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)

@main.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    if request.method == 'POST':
        current_user.name = request.form.get('name')
        current_user.degree = request.form.get('degree')
        current_user.units = request.form.get('units')
        current_user.availability = request.form.get('availability')
        current_user.study_style = request.form.get('study_style')
        current_user.study_preferences = request.form.get('study_preferences')
        current_user.open_to_teams = True if request.form.get('open_to_teams') == 'yes' else False
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('main.profile'))
    return render_template('edit_profile.html', user=current_user)

@main.route('/sessions')
@login_required
def sessions():
    return render_template('study_sessions.html')

@main.route('/create_session', methods=['GET', 'POST'])
@login_required
def create_session():
    return render_template('create_session.html')

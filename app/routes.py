from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models import User, StudySession
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
    all_sessions = StudySession.query.all()
    return render_template('study_sessions.html', sessions=all_sessions)

@main.route('/create_session', methods=['GET', 'POST'])
@login_required
def create_session():
    if request.method == 'POST':
        session = StudySession(
            title=request.form.get('name'),
            unit=request.form.get('unit'),
            date=request.form.get('date'),
            time=request.form.get('time'),
            location=request.form.get('location'),
            mode=request.form.get('mode'),
            max_spots=request.form.get('max_participants', 6),
            creator_id=current_user.id
        )
        db.session.add(session)
        db.session.commit()
        flash('Session created successfully!', 'success')
        return redirect(url_for('main.sessions'))
    return render_template('create_session.html')

@main.route('/sessions/<int:session_id>/join', methods=['POST'])
@login_required
def join_session(session_id):
    session = StudySession.query.get_or_404(session_id)
    if current_user in session.participants:
        flash('You have already joined this session!', 'warning')
    elif len(session.participants) >= session.max_spots:
        flash('This session is full!', 'danger')
    else:
        session.participants.append(current_user)
        db.session.commit()
        flash('Successfully joined the session!', 'success')
    return redirect(url_for('main.sessions'))
@main.route('/sessions/<int:session_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_session(session_id):
    session = StudySession.query.get_or_404(session_id)

    # Only creator can edit
    if session.creator_id != current_user.id:
        flash('You can only edit sessions you created.', 'danger')
        return redirect(url_for('main.sessions'))

    if request.method == 'POST':
        session.title = request.form.get('name')
        session.unit = request.form.get('unit')
        session.date = request.form.get('date')
        session.time = request.form.get('time')
        session.location = request.form.get('location')
        session.mode = request.form.get('mode')
        session.max_spots = int(request.form.get('max_participants') or 6)

        db.session.commit()

        flash('Session updated successfully!', 'success')
        return redirect(url_for('main.sessions'))

    return render_template('edit_session.html', session=session)
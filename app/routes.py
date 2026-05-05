from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models import User, StudySession, BuddyRequest
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
    sent_requests = [r.receiver_id for r in current_user.sent_requests]
    return render_template('browse_users.html', users=users, sent_requests=sent_requests)

@main.route('/profile')
@login_required
def profile():
    incoming_requests = BuddyRequest.query.filter_by(
        receiver_id=current_user.id,
        status='pending'
    ).all()
    accepted_sent = BuddyRequest.query.filter_by(
        sender_id=current_user.id,
        status='accepted'
    ).all()
    accepted_received = BuddyRequest.query.filter_by(
        receiver_id=current_user.id,
        status='accepted'
    ).all()
    buddies = [r.receiver for r in accepted_sent] + [r.sender for r in accepted_received]
    return render_template('profile.html', user=current_user,
                          incoming_requests=incoming_requests,
                          buddies=buddies)

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

@main.route('/send_request/<int:user_id>', methods=['POST'])
@login_required
def send_request(user_id):
    existing = BuddyRequest.query.filter_by(
        sender_id=current_user.id,
        receiver_id=user_id
    ).first()
    if existing:
        flash('Request already sent!', 'warning')
    else:
        request_obj = BuddyRequest(
            sender_id=current_user.id,
            receiver_id=user_id
        )
        db.session.add(request_obj)
        db.session.commit()
        flash('Buddy request sent!', 'success')
    return redirect(url_for('main.browse'))

@main.route('/accept_request/<int:request_id>', methods=['POST'])
@login_required
def accept_request(request_id):
    req = BuddyRequest.query.get_or_404(request_id)
    req.status = 'accepted'
    db.session.commit()
    flash('Buddy request accepted!', 'success')
    return redirect(url_for('main.profile'))

@main.route('/decline_request/<int:request_id>', methods=['POST'])
@login_required
def decline_request(request_id):
    req = BuddyRequest.query.get_or_404(request_id)
    req.status = 'declined'
    db.session.commit()
    flash('Buddy request declined.', 'info')
    return redirect(url_for('main.profile'))

@main.route('/buddies')
@login_required
def buddies():
    accepted_sent = BuddyRequest.query.filter_by(
        sender_id=current_user.id,
        status='accepted'
    ).all()
    accepted_received = BuddyRequest.query.filter_by(
        receiver_id=current_user.id,
        status='accepted'
    ).all()
    buddies = [r.receiver for r in accepted_sent] + [r.sender for r in accepted_received]
    return render_template('buddies.html', buddies=buddies)

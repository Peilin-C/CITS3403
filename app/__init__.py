from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'danger'

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    from app.routes import main
    from app.auth import auth
    app.register_blueprint(main)
    app.register_blueprint(auth)

    with app.app_context():
        db.create_all()

    @app.context_processor
    def inject_counts():
        from flask_login import current_user
        if current_user.is_authenticated:
            from app.models import BuddyRequest, Message
            pending = BuddyRequest.query.filter_by(
                receiver_id=current_user.id,
                status='pending'
            ).count()
            unread = Message.query.filter_by(
                receiver_id=current_user.id,
                is_read=False
            ).count()
            return {'pending_requests': pending, 'unread_messages': unread}
        return {'pending_requests': 0, 'unread_messages': 0}

    return app

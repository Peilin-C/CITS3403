from app import create_app, db
from app.models import User

app = create_app()

def create_demo_users():
    with app.app_context():
        if User.query.count() == 0:
            demo_users = [
                {
                    'name': 'Alex Johnson',
                    'email': 'alex@student.uwa.edu.au',
                    'degree': 'Computer Science',
                    'units': 'CITS3403, CITS3002',
                    'availability': 'Morning',
                    'study_style': 'Group study',
                    'open_to_teams': True
                },
                {
                    'name': 'Sarah Chen',
                    'email': 'sarah@student.uwa.edu.au',
                    'degree': 'Engineering',
                    'units': 'CITS3403, ENGT2000',
                    'availability': 'Evening',
                    'study_style': 'Quiet study',
                    'open_to_teams': False
                },
                {
                    'name': 'James Wilson',
                    'email': 'james@student.uwa.edu.au',
                    'degree': 'Commerce',
                    'units': 'CITS3403, BUSN2001',
                    'availability': 'Weekends',
                    'study_style': 'Online study',
                    'open_to_teams': True
                },
                {
                    'name': 'Priya Patel',
                    'email': 'priya@student.uwa.edu.au',
                    'degree': 'Science',
                    'units': 'CITS3403, CITS3001',
                    'availability': 'Afternoon',
                    'study_style': 'In-person study',
                    'open_to_teams': False
                },
                {
                    'name': 'Liam Thompson',
                    'email': 'liam@student.uwa.edu.au',
                    'degree': 'Computer Science',
                    'units': 'CITS3403, CITS3200',
                    'availability': 'Morning',
                    'study_style': 'Group study',
                    'open_to_teams': True
                },
                {
                    'name': 'Emma Davis',
                    'email': 'emma@student.uwa.edu.au',
                    'degree': 'Arts',
                    'units': 'CITS3403, ARTS2000',
                    'availability': 'Weekends',
                    'study_style': 'Quiet study',
                    'open_to_teams': False
                },
            ]
            for u in demo_users:
                user = User(
                    name=u['name'],
                    email=u['email'],
                    degree=u['degree'],
                    units=u['units'],
                    availability=u['availability'],
                    study_style=u['study_style'],
                    open_to_teams=u['open_to_teams']
                )
                user.set_password('Password123')
                db.session.add(user)
            db.session.commit()
            print('✅ Demo users created!')

create_demo_users()

if __name__ == '__main__':
    app.run(debug=True)
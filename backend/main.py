from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os
from prisma import Prisma
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.backend.training_creator import TrainingCreator
from src.backend.training_manager import TrainingManager
from src.backend.user_manager import UserManager

db = Prisma()
db.connect()

app = Flask(__name__)
CORS(app, origins="*")

training_creator = TrainingCreator()
training_manager = TrainingManager()
user_manager = UserManager()

#-------------- display training ----------------

# Sample data for demo --> Replace with new ones

sample_trainings = {
    'Sailing': [
        {'id': 1, 'name': 'Kitesurfing', 'field': 'Sailing'},
    ],
    'Other': [
        {'id': 4, 'name': 'Middle east', 'field': 'Other'},
        {'id': 5, 'name': 'Marathon Prep', 'field': 'Other'},
        {'id': 6, 'name': 'React Programming', 'field': 'Other'},
    ]
}

#-------------------------------


@app.route('/training', methods=['GET'])
def get_training():
    field = request.args.get('field')
    
    # If a field is specified, return trainings for that field
    if field and field in sample_trainings:
        return jsonify(sample_trainings[field])
    
    # If no field is specified or field not found, return all trainings
    all_trainings = []
    for trainings in sample_trainings.values():
        all_trainings.extend(trainings)
    
    return jsonify(all_trainings)





logged_user = None # Placeholder for logged-in user

@app.route('/login', methods=['POST'])
def login():
    global logged_user
    data = request.get_json()

    username = data.get('username')
    phone = data.get('phone')

    if not username:
        return jsonify({'error': 'Username required'}), 400
    if not phone:
        return jsonify({'error': 'Phone number required'}), 400

    try:
        # Check if user exists with this phone number
        user = user_manager.get_user_by_phone(phone)
        if user:
            if user.username != username:
                return jsonify({'error': 'Phone number already registered to a different user'}), 400
        else:
            # Create new user if phone number is not in use
            user = user_manager.create_user(username, phone)

        logged_user = username
        return jsonify({
            'message': f'User {username} logged in successfully',
            'username': username,
            'phone': phone
        })
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        print(f"Login error: {str(e)}")  # Add logging
        return jsonify({'error': 'An error occurred during login'}), 500


if __name__ == '__main__':
    app.run(debug=True, port = 8080)
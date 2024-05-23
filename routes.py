from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from models.models import Exercise
from models.database import db
from __main__ import app

def authenticate(username, password):
    users = {
        'writer': 'writer',
        'admin': 'admin'
    }
    if username in users and users[username] == password:
        return username

def admin_required(fn):
    def wrapper(*args, **kwargs):
        current_user = get_jwt_identity()
        if current_user != 'admin':
            return jsonify({"error": "Admin access required"}), 401
        return fn(*args, **kwargs)
    return wrapper

@app.route('/token', methods=['POST'])
def get_token():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if username and password:
        if authenticate(username, password):
            access_token = create_access_token(identity=username)
            return jsonify({'Bearer': access_token}), 200
        else:
            return jsonify({'error': 'Invalid username or password'}), 401
    else:
        return jsonify({'error': 'Username and password required'}), 400

@app.route('/exercises', methods=['GET'])
@jwt_required()
def get_exercises():
    current_user = get_jwt_identity()
    role = 'WRITER' if current_user == 'writer' else 'ADMIN'

    if role not in ['ADMIN', 'WRITER']:
        return jsonify({"msg": "Not allowed"}), 403
    
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=5, type=int)

    difficulty = request.args.get('difficulty')

    if difficulty:
        exercises = Exercise.query.filter_by(difficulty=difficulty)\
                                   .paginate(page=page, per_page=per_page, error_out=False)
    else:
        exercises = Exercise.query.paginate(page=page, per_page=per_page, error_out=False)

    if not exercises:
        return jsonify({"msg": "No exercises found"}), 404
    
    data = [exercise.to_dict() for exercise in exercises.items]
    pagination_data = {
        'total_pages': exercises.pages,
        'total_items': exercises.total,
        'current_page': exercises.page,
        'per_page': exercises.per_page,
        'next_page': exercises.next_num,
        'prev_page': exercises.prev_num,
        'exercises': data
    }

    return jsonify(pagination_data), 200


@app.route('/exercises/<int:id>', methods=['GET'])
@jwt_required()
def get_exercise_by_id(id):
    current_user = get_jwt_identity()

    role = 'WRITER' if current_user == 'writer' else 'ADMIN'

    if role not in ['ADMIN', 'WRITER']:
        return jsonify({"msg": "Not allowed"}), 403

    exercise = Exercise.query.get_or_404(id)
    if exercise:
        return jsonify(exercise.to_dict()), 200
    else:
        return jsonify({'error': 'Exercise not found'}), 404


@app.route('/exercises', methods=['POST'])
@jwt_required()
def create_exercise():
    current_user = get_jwt_identity()

    role = 'WRITER' if current_user == 'writer' else 'ADMIN'

    if role not in ['ADMIN', 'WRITER']:
        return jsonify({"msg": "Not allowed"}), 403

    data = request.get_json()
    new_exercise = Exercise(**data)
    db.session.add(new_exercise)
    db.session.commit()

    return jsonify({"message": "Exercise created successfully"}), 201

@app.route('/exercises/<int:id>', methods=['PUT'])
@jwt_required()
def update_exercise(id):
    current_user = get_jwt_identity()

    role = 'WRITER' if current_user == 'writer' else 'ADMIN'

    if role not in ['ADMIN', 'WRITER']:
        return jsonify({"msg": "Not allowed"}), 403

    data = request.get_json()
    exercise = Exercise.query.get_or_404(id)

    for key, value in data.items():
        setattr(exercise, key, value)

    db.session.commit()

    return jsonify({"message": "Exercise updated successfully"}), 200

@app.route('/exercises/<int:id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_exercise(id):
    exercise = Exercise.query.get_or_404(id)
    db.session.delete(exercise)
    db.session.commit()

    return jsonify({"message": "Exercise deleted successfully"}), 200

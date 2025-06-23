from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, create_access_token
from models import db, User, Guest, Episode, Appearance

controllers_bp = Blueprint('controllers', __name__)

# AUTH routes
@controllers_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    user = User(username=data['username'])
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User registered successfully"}), 201

@controllers_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(username=data['username']).first()
    if user and user.check_password(data['password']):
        token = create_access_token(identity=user.id)
        return jsonify({"token": token}), 200
    return jsonify({"error": "Invalid credentials"}), 401

# GUEST routes
@controllers_bp.route('/guests', methods=['GET'])
def get_guests():
    guests = Guest.query.all()
    return jsonify([{"id": g.id, "name": g.name, "occupation": g.occupation} for g in guests]), 200

# EPISODE routes
@controllers_bp.route('/episodes', methods=['GET'])
def get_episodes():
    episodes = Episode.query.all()
    return jsonify([{"id": e.id, "date": e.date.isoformat(), "number": e.number} for e in episodes]), 200

@controllers_bp.route('/episodes/<int:id>', methods=['GET'])
def get_episode(id):
    episode = Episode.query.get_or_404(id)
    appearances = [{
        "id": a.id,
        "guest": {"id": a.guest.id, "name": a.guest.name},
        "rating": a.rating
    } for a in episode.appearances]
    return jsonify({"id": episode.id, "date": episode.date.isoformat(), "number": episode.number, "appearances": appearances}), 200

@controllers_bp.route('/episodes/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_episode(id):
    episode = Episode.query.get_or_404(id)
    db.session.delete(episode)
    db.session.commit()
    return jsonify({"message": "Episode deleted"}), 200

# APPEARANCE routes
@controllers_bp.route('/appearances', methods=['POST'])
@jwt_required()
def create_appearance():
    data = request.json
    rating = data.get('rating')
    guest_id = data.get('guest_id')
    episode_id = data.get('episode_id')

    if not (1 <= rating <= 5):
        return jsonify({"error": "Rating must be between 1 and 5"}), 400

    appearance = Appearance(rating=rating, guest_id=guest_id, episode_id=episode_id)
    db.session.add(appearance)
    db.session.commit()

    return jsonify({"message": "Appearance created", "id": appearance.id}), 201

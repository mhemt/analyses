import json

from flask import request, jsonify, abort

from app import app
from database import db_session
from models import User


@app.route(f'{app.api_path}/users/', methods=['GET', 'POST'])
def api_users():
    if request.method == 'GET':
        users = User.query.all()

        return jsonify([dict(
            id=user.id,
            username=user.username,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            type=user.type.value,
        ) for user in users])

    elif request.method == 'POST':
        data = json.loads(request.data)

        user = User(
            username=data['username'],
            email=data['email'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            type=data['type'],
        )

        db_session.add(user)
        db_session.commit()

        return jsonify(
            id=user.id,
            username=user.username,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            type=user.type.value,
        )


@app.route(f'{app.api_path}/users/<int:user_id>', methods=['GET', 'PUT', 'PATCH', 'DELETE'])
def api_user(user_id: int):
    if request.method == 'GET':
        user = User.query.filter(User.id == user_id).first()

        if user is None:
            abort(404)

        return jsonify(
            id=user.id,
            username=user.username,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            type=user.type.value,
        )

    elif request.method in ('PUT', 'PATCH'):
        data = json.loads(request.data)
        user = User.query.filter(User.id == user_id).first()

        if user is None:
            abort(404)

        user.username = data.get('username') or user.username
        user.email = data.get('email') or user.email
        user.first_name = data.get('first_name') or user.first_name
        user.last_name = data.get('last_name') or user.last_name

        db_session.commit()

        return jsonify(
            id=user.id,
            username=user.username,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            type=user.type.value,
        )

    elif request.method == 'DELETE':
        user = User.query.filter(User.id == user_id).first()

        db_session.delete(user)
        db_session.commit()

        return jsonify(
            id=user.id,
            username=user.username,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            type=user.type.value,
        )

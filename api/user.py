import json

from flask import request, jsonify, abort, Response

from app import app
from database import db_session
from models import User, get_all, get_by_id, delete_by_id, create, update_by_id


@app.route(f'{app.api_path}/users/', methods=['GET', 'POST'])
def api_users() -> Response:
    if request.method == 'GET':
        users = get_all(User, db_session)

        return jsonify(users)

    elif request.method == 'POST':
        data = json.loads(request.data)
        user = create(User, db_session, data)

        return jsonify(user)


@app.route(f'{app.api_path}/users/<int:user_id>', methods=['GET', 'PUT', 'PATCH', 'DELETE'])
def api_user(user_id: int) -> Response:
    if request.method == 'GET':
        user = get_by_id(User, db_session, user_id)

        if user is None:
            abort(404)

        return jsonify(user)

    elif request.method in ('PUT', 'PATCH'):
        data = json.loads(request.data)

        try:
            user = update_by_id(User, db_session, user_id, data)
        except ValueError:
            abort(400)
        else:
            if user is None:
                abort(404)

            return jsonify(user)

    elif request.method == 'DELETE':
        user = delete_by_id(User, db_session, user_id)

        if user is None:
            abort(404)

        return jsonify(user)

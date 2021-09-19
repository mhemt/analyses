import json

from flask import request, jsonify, abort

from app import app
from database import db_session
from models import Laboratory


@app.route(f'{app.api_path}/labs/', methods=['GET', 'POST'])
def api_labs():
    if request.method == 'GET':
        labs = Laboratory.query.all()

        return jsonify([dict(
            id=lab.id,
            name=lab.username,
            address=lab.email,
        ) for lab in labs])

    elif request.method == 'POST':
        data = json.loads(request.data)

        lab = Laboratory(
            name=data['name'],
            address=data['address'],
        )

        db_session.add(lab)
        db_session.commit()

        return jsonify(
            id=lab.id,
            name=lab.name,
            address=lab.address,
        )


@app.route(f'{app.api_path}/labs/<int:lab_id>', methods=['GET', 'PUT', 'PATCH', 'DELETE'])
def api_lab(lab_id: int):
    if request.method == 'GET':
        lab = Laboratory.query.filter(Laboratory.id == lab_id).first()

        if lab is None:
            abort(404)

        return jsonify(
            id=lab.id,
            name=lab.name,
            address=lab.address,
        )

    elif request.method in ('PUT', 'PATCH'):
        data = json.loads(request.data)
        lab = Laboratory.query.filter(Laboratory.id == lab_id).first()

        if lab is None:
            abort(404)

        lab.name = data.get('name') or lab.name
        lab.address = data.get('address') or lab.address

        db_session.commit()

        return jsonify(
            id=lab.id,
            name=lab.name,
            address=lab.address,
        )

    elif request.method == 'DELETE':
        lab = Laboratory.query.filter(Laboratory.id == lab_id).first()

        db_session.delete(lab)
        db_session.commit()

        return jsonify(
            id=lab.id,
            name=lab.name,
            address=lab.address,
        )

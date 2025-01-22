#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from models import db, User, Review, Game, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return "Index for Game/Review/User API"

# Existing routes remain unchanged ...

@app.route('/baked_goods', methods=['POST'])
def create_baked_good():
    # Create a new baked good
    try:
        new_baked_good = BakedGood(
            name=request.form.get("name"),
            price=float(request.form.get("price")),
            bakery_id=int(request.form.get("bakery_id"))
        )
        db.session.add(new_baked_good)
        db.session.commit()

        response = make_response(new_baked_good.to_dict(), 201)
        return response

    except Exception as e:
        response = make_response({"error": str(e)}, 400)
        return response

@app.route('/bakeries/<int:id>', methods=['PATCH'])
def update_bakery_name(id):
    # Update the name of the bakery
    bakery = Bakery.query.filter_by(id=id).first()

    if not bakery:
        response = make_response({"message": "Bakery not found."}, 404)
        return response

    new_name = request.form.get("name")
    if new_name:
        bakery.name = new_name
        db.session.commit()

        response = make_response(bakery.to_dict(), 200)
        return response
    else:
        response = make_response({"message": "No name provided."}, 400)
        return response

@app.route('/baked_goods/<int:id>', methods=['DELETE'])
def delete_baked_good(id):
    # Delete a baked good
    baked_good = BakedGood.query.filter_by(id=id).first()

    if not baked_good:
        response = make_response({"message": "Baked good not found."}, 404)
        return response

    db.session.delete(baked_good)
    db.session.commit()

    response = make_response(
        {"message": f"Baked good with id {id} deleted successfully."},
        200
    )
    return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)

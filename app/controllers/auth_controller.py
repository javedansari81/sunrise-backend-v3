# app/controllers/auth_controller.py
from flask import request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask import current_app as app
from app.models.user_model import UserModel
from bson import ObjectId
from app import mongo

user_model = UserModel(mongo)

def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    # Find the user by email
    user = user_model.find_one({"email": email})
    if not user:
        return jsonify({"msg": "Invalid email or password"}), 401
    
    # Check if password is hashed (starts with $2b$)
    if user["password"].startswith("$2b$"):
        # Verify hashed password
        password_correct = app.bcrypt.check_password_hash(user["password"], password)
    else:
        # Plain text comparison (for development only)
        password_correct = user["password"] == password
    
    if not password_correct:
        return jsonify({"msg": "Invalid email or password"}), 401

    # Create JWT token
    access_token = create_access_token(identity=str(user["_id"]))
    user_details = {
            'id': str(user['_id']),
            'email': user['email'],
            'firstName': user['firstName'],
            'lastName': user['lastName'],
            'mobile': user['mobile'],
            'userType': user['userType']
        }
    return jsonify({
            'access_token': access_token,
            'user': user_details
        }), 200

@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from flask_migrate import Migrate
from models import db, Message
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)

migrate = Migrate(app, db)
db.init_app(app)

@app.route('/messages', methods=['GET'])
def get_messages():
    messages = Message.query.order_by(Message.created_at.asc()).all()
    return jsonify([message.to_dict() for message in messages])

@app.route('/messages', methods=['POST'])
def create_message():
    data = request.get_json()
    
    # Create new message with data from request
    new_message = Message(
        body=data.get('body'),
        username=data.get('username')
    )
    
    # Add and commit to database
    db.session.add(new_message)
    db.session.commit()
    
    # Return the new message as JSON
    return jsonify(new_message.to_dict()), 201

@app.route('/messages/<int:id>', methods=['PATCH'])
def update_message(id):
    message = Message.query.get(id)
    
    if not message:
        return jsonify({"error": "Message not found"}), 404
    
    data = request.get_json()
    
    # Update message body
    if 'body' in data:
        message.body = data['body']
    
    # Commit changes
    db.session.commit()
    
    return jsonify(message.to_dict())

@app.route('/messages/<int:id>', methods=['DELETE'])
def delete_message(id):
    message = Message.query.get(id)
    
    if not message:
        return jsonify({"error": "Message not found"}), 404
    
    # Delete the message
    db.session.delete(message)
    db.session.commit()
    
    return "", 204

if __name__ == '__main__':
    app.run(port=5000, debug=True)
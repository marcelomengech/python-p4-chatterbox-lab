#!/usr/bin/env python3

from app import app
from models import db, Message
from datetime import datetime

with app.app_context():
    print("Deleting existing messages...")
    Message.query.delete()
    
    print("Creating messages...")
    
    messages = [
        Message(
            body="Hello, World!",
            username="Alice",
            created_at=datetime(2023, 1, 1, 12, 0, 0),
            updated_at=datetime(2023, 1, 1, 12, 0, 0)
        ),
        Message(
            body="Flask is awesome!",
            username="Bob",
            created_at=datetime(2023, 1, 1, 12, 5, 0),
            updated_at=datetime(2023, 1, 1, 12, 5, 0)
        ),
        Message(
            body="Learning full-stack development",
            username="Charlie",
            created_at=datetime(2023, 1, 1, 12, 10, 0),
            updated_at=datetime(2023, 1, 1, 12, 10, 0)
        )
    ]
    
    db.session.add_all(messages)
    db.session.commit()
    
    print("Seeding complete!")
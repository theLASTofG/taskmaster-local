from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20))
    profile_image = db.Column(db.String(255))
    bio = db.Column(db.Text)
    rating = db.Column(db.Float, default=0.0)
    total_tasks_completed = db.Column(db.Integer, default=0)
    total_tasks_created = db.Column(db.Integer, default=0)
    is_tasker = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    created_tasks = db.relationship('Task', foreign_keys='Task.client_id', backref='client', lazy='dynamic')
    assigned_tasks = db.relationship('Task', foreign_keys='Task.tasker_id', backref='tasker', lazy='dynamic')
    applications = db.relationship('TaskApplication', backref='applicant', lazy='dynamic')
    sent_messages = db.relationship('Message', foreign_keys='Message.sender_id', backref='sender', lazy='dynamic')
    received_messages = db.relationship('Message', foreign_keys='Message.receiver_id', backref='receiver', lazy='dynamic')
    given_reviews = db.relationship('Review', foreign_keys='Review.reviewer_id', backref='reviewer', lazy='dynamic')
    received_reviews = db.relationship('Review', foreign_keys='Review.reviewed_id', backref='reviewed', lazy='dynamic')

    def __repr__(self):
        return f'<User {self.email}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'phone': self.phone,
            'profile_image': self.profile_image,
            'bio': self.bio,
            'rating': self.rating,
            'total_tasks_completed': self.total_tasks_completed,
            'total_tasks_created': self.total_tasks_created,
            'is_tasker': self.is_tasker,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

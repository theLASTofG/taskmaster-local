from src.models.user import db
from datetime import datetime

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    location_address = db.Column(db.String(255), nullable=False)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, assigned, in_progress, completed, cancelled
    client_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    tasker_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    scheduled_date = db.Column(db.DateTime)
    estimated_duration = db.Column(db.String(50))

    # Relationships
    applications = db.relationship('TaskApplication', backref='task', lazy='dynamic')
    messages = db.relationship('Message', backref='task', lazy='dynamic')
    reviews = db.relationship('Review', backref='task', lazy='dynamic')
    payments = db.relationship('Payment', backref='task', lazy='dynamic')

    def __repr__(self):
        return f'<Task {self.title}>'

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'category': self.category,
            'location_address': self.location_address,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'price': self.price,
            'status': self.status,
            'client_id': self.client_id,
            'tasker_id': self.tasker_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'scheduled_date': self.scheduled_date.isoformat() if self.scheduled_date else None,
            'estimated_duration': self.estimated_duration,
            'client': self.client.to_dict() if self.client else None,
            'tasker': self.tasker.to_dict() if self.tasker else None
        }

class TaskApplication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=False)
    tasker_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message = db.Column(db.Text)
    proposed_price = db.Column(db.Float)
    status = db.Column(db.String(20), default='pending')  # pending, accepted, rejected
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<TaskApplication {self.id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'task_id': self.task_id,
            'tasker_id': self.tasker_id,
            'message': self.message,
            'proposed_price': self.proposed_price,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'applicant': self.applicant.to_dict() if self.applicant else None
        }


from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin



db = SQLAlchemy()



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)  
    status = db.Column(db.String(20), default='pending') 
    profile_verified = db.Column(db.Boolean, default=False)  
    service_requests = db.relationship(
        'ServiceRequest',
        foreign_keys='ServiceRequest.customer_id',
        backref='customer_request',  
        lazy=True
    )
    assigned_requests = db.relationship(
        'ServiceRequest',
        foreign_keys='ServiceRequest.professional_id',
        backref='professional_assignment', 
        lazy=True
    )
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.role}', '{self.status}', '{self.profile_verified}')"




class Service(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    base_price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200))
    service_requests = db.relationship(
        'ServiceRequest', 
        backref='linked_service',  
        lazy=True
    )
    def __repr__(self):
        return f"Service('{self.name}', '{self.base_price}')"



class ServiceRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(50), default='pending')
    location = db.Column(db.String(100), nullable=False)
    remarks = db.Column(db.String(200))
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    professional_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    review = db.Column(db.String(255), nullable=True)
    rating = db.Column(db.Integer, nullable=True)  
    customer = db.relationship('User', foreign_keys=[customer_id])
    professional = db.relationship('User', foreign_keys=[professional_id])
    service = db.relationship('Service')
    def __repr__(self):
        return f"ServiceRequest('{self.status}', '{self.location}', '{self.review}', '{self.rating}')"

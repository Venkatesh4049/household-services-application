from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import ServiceRequest, ServiceProfessional

professional_bp = Blueprint('professional', __name__)

@professional_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'professional':
        return redirect(url_for('auth.login'))
    # Get the professional's ID
    professional = ServiceProfessional.query.filter_by(user_id=current_user.id).first()
    if not professional:
        flash("Professional profile not found.")
        return redirect(url_for('auth.login'))
    # Get service requests assigned to this professional
    service_requests = ServiceRequest.query.filter_by(professional_id=professional.id).all()
    return render_template('professional/dashboard.html', service_requests=service_requests)

@professional_bp.route('/request/accept/<int:id>', methods=['POST'])
@login_required
def accept_request(id):
    if current_user.role != 'professional':
        return redirect(url_for('auth.login'))
    service_request = ServiceRequest.query.get(id)
    if service_request and service_request.status == 'requested':
        service_request.status = 'assigned'
        db.session.commit()
        flash('Service request accepted.')
    return redirect(url_for('professional.dashboard'))

@professional_bp.route('/request/close/<int:id>', methods=['POST'])
@login_required
def close_request(id):
    if current_user.role != 'professional':
        return redirect(url_for('auth.login'))
    service_request = ServiceRequest.query.get(id)
    if service_request and service_request.status == 'assigned':
        service_request.status = 'closed'
        db.session.commit()
        flash('Service request closed.')
    return redirect(url_for('professional.dashboard'))

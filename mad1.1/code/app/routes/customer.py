from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import Service, ServiceRequest

customer_bp = Blueprint('customer', __name__)

@customer_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'customer':
        return redirect(url_for('auth.login'))
    services = Service.query.all()
    service_requests = ServiceRequest.query.filter_by(customer_id=current_user.id).all()
    return render_template('customer/dashboard.html', services=services, service_requests=service_requests)

@customer_bp.route('/request/new', methods=['GET', 'POST'])
@login_required
def create_request():
    if current_user.role != 'customer':
        return redirect(url_for('auth.login'))
    if request.method == 'POST':
        service_id = request.form['service_id']
        date_of_request = request.form['date_of_request']
        new_request = ServiceRequest(
            service_id=service_id,
            customer_id=current_user.id,
            date_of_request=date_of_request,
            status='requested'
        )
        db.session.add(new_request)
        db.session.commit()
        flash('Service request created successfully.')
        return redirect(url_for('customer.dashboard'))
    services = Service.query.all()
    return render_template('customer/create_request.html', services=services)

@customer_bp.route('/request/review/<int:id>', methods=['POST'])
@login_required
def review_request(id):
    if current_user.role != 'customer':
        return redirect(url_for('auth.login'))
    service_request = ServiceRequest.query.get(id)
    if service_request and service_request.customer_id == current_user.id and service_request.status == 'closed':
        service_request.remarks = request.form['remarks']
        db.session.commit()
        flash('Review submitted.')
    return redirect(url_for('customer.dashboard'))

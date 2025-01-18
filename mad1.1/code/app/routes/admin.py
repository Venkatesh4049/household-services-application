from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import User, Service

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'admin':
        return redirect(url_for('auth.login'))
    services = Service.query.all()
    return render_template('admin/dashboard.html', services=services)

@admin_bp.route('/service/new', methods=['GET', 'POST'])
@login_required
def create_service():
    if current_user.role != 'admin':
        return redirect(url_for('auth.login'))
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        description = request.form['description']
        time_required = request.form['time_required']
        new_service = Service(name=name, price=price, description=description, time_required=time_required)
        db.session.add(new_service)
        db.session.commit()
        flash('Service created successfully.')
        return redirect(url_for('admin.dashboard'))
    return render_template('admin/create_service.html')

@admin_bp.route('/user/approve/<int:id>', methods=['POST'])
@login_required
def approve_user(id):
    if current_user.role != 'admin':
        return redirect(url_for('auth.login'))
    user = User.query.get(id)
    if user:
        user.status = 'approved'
        db.session.commit()
        flash(f'User {user.username} approved.')
    return redirect(url_for('admin.dashboard'))


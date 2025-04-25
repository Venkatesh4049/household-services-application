from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from models import db, User, Service, ServiceRequest 
from forms import LoginForm, RegisterForm, ServiceForm, ServiceRequestForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf.csrf import CSRFProtect
from functools import wraps
from sqlalchemy import inspect
from forms import BlockApproveForm
from sqlalchemy import text
from flask_migrate import Migrate



csrf = CSRFProtect()
app = Flask(__name__)



app.config.from_object('config.Config')
app.config['SECRET_KEY'] = 'your_secret_key' 
app.config['WTF_CSRF_ENABLED'] = False  
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///D:/IITM/NEW/Chatgpt2/code/instance/site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False



db.init_app(app)
migrate = Migrate(app, db)



login_manager = LoginManager(app)
login_manager.login_view = 'login'



csrf.init_app(app)



def check_user_status(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated and current_user.status == 'blocked':
            flash('Your account is currently blocked. Please contact the administrator.', 'warning')
            return redirect(url_for('login')) 
        return f(*args, **kwargs)
    return decorated_function



@app.before_first_request
def create_tables():
    inspector = inspect(db.engine)
    columns = [col['name'] for col in inspector.get_columns('user')] 
    if 'profile_verified' not in columns:
        with app.app_context():
            db.session.execute(text('ALTER TABLE user ADD COLUMN profile_verified BOOLEAN DEFAULT FALSE'))
            db.session.commit()
    db.create_all()
    


@app.before_request
def initialize_admin():
    admin_user = User.query.filter_by(username='admin').first()
    if not admin_user:
        admin_password = generate_password_hash('admin123', method='sha256')
        admin = User(username='admin', email='admin@example.com', password=admin_password, role='admin')
        db.session.add(admin)
        db.session.commit()



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



@app.route('/')
def home():
    return redirect(url_for('login'))



@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            if user.status == 'blocked':
                flash('Your account is blocked. Please contact the administrator.', 'danger')
                return redirect(url_for('login'))
            login_user(user)
            flash('Login successful!', 'success')
            if user.role == 'admin':
                return redirect(url_for('admin_dashboard'))
            elif user.role == 'professional':
                return redirect(url_for('professional_dashboard'))
            else:
                return redirect(url_for('customer_dashboard'))
        else:
            flash('Invalid email or password.', 'danger')
    return render_template('login.html', form=form)



@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.role.data not in ['customer', 'professional']:
            flash('Invalid role selected. Please choose either Customer or Professional.', 'danger')
            return render_template('register.html', form=form)
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash('Username already exists. Please choose a different one.', 'danger')
            return render_template('register.html', form=form)
        existing_email = User.query.filter_by(email=form.email.data).first()
        if existing_email:
            flash('Email already registered. Please use a different email or log in.', 'danger')
            return render_template('register.html', form=form)
        hashed_password = generate_password_hash(form.password.data) 
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_password,
            role=form.role.data
        )
        db.session.add(user)
        db.session.commit()
        flash('Account created successfully!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        flash('You are not authorized to access this page.', 'danger')
        return redirect(url_for('login'))
    form = BlockApproveForm()
    users = User.query.all()  
    all_requests = ServiceRequest.query.all()
    professionals = User.query.filter_by(role='professional').all()
    reviews = {}    
    for professional in professionals:
        reviews[professional.id] = ServiceRequest.query.filter_by(professional_id=professional.id, status='completed').all()
    return render_template('admin_dashboard.html', users=users, form=form, professionals=professionals, reviews=reviews, all_requests=all_requests)


@app.route('/admin/close_service_request/<int:request_id>', methods=['POST'])
@login_required
def close_service_request(request_id):
    if current_user.role != 'admin':
        flash('You are not authorized to access this page.', 'danger')
        return redirect(url_for('login'))
    service_request = ServiceRequest.query.get_or_404(request_id)
    service_request.status = 'closed'
    db.session.commit()
    flash('Service request has been closed.', 'success')
    return redirect(url_for('admin_dashboard'))



@app.route('/admin/create_service', methods=['GET', 'POST'])
@login_required
def create_service():
    if current_user.role != 'admin':
        flash('You are not authorized to access this page.', 'danger')
        return redirect(url_for('login'))
    form = ServiceForm()
    if form.validate_on_submit():
        service = Service(
            name=form.name.data,
            base_price=form.base_price.data,
            description=form.description.data
        )
        db.session.add(service)
        db.session.commit()
        flash('Service created successfully!', 'success')
        return redirect(url_for('admin_dashboard'))
    return render_template('create_service.html', form=form)



@app.route('/admin/block_user/<int:user_id>', methods=['POST'])
@login_required
def block_user(user_id):
    if current_user.role != 'admin':
        flash('You are not authorized to access this page.', 'danger')
        return redirect(url_for('login'))
    user = db.session.get(User, user_id)
    if user and user.role != 'admin': 
        user.status = 'blocked'
        db.session.commit() 
        flash(f'User {user.username} has been blocked.', 'success')
    else:
        flash('User not found or invalid operation.', 'danger')
    return redirect(url_for('admin_dashboard'))



@app.route('/admin/approve_user/<int:user_id>', methods=['POST'])
@login_required
def approve_user(user_id):
    if current_user.role != 'admin':
        flash('You are not authorized to access this page.', 'danger')
        return redirect(url_for('login'))
    user = User.query.get(user_id)
    if user and user.role == 'professional' and user.status == 'pending':
        user.status = 'approved'  
        user.profile_verified = True 
        db.session.commit() 
        flash(f"Professional '{user.username}' has been approved.", "success")
    else:
        flash("User is not eligible for approval.", "warning")
    return redirect(url_for('admin_dashboard'))  



@app.route('/admin/services')
@login_required
def admin_services():
    if current_user.role != 'admin':
        flash('You do not have permission to view this page.', 'danger')
        return redirect(url_for('index'))
    services = Service.query.all()
    return render_template('admin_services.html', services=services)



@app.route('/admin/service/edit/<int:service_id>', methods=['GET', 'POST'])
@login_required
def edit_service(service_id):
    if current_user.role != 'admin':
        flash('You do not have permission to edit this service.', 'danger')
        return redirect(url_for('admin_services'))
    service = Service.query.get_or_404(service_id)
    if request.method == 'POST':
        service.name = request.form['name']
        service.description = request.form['description']
        db.session.commit()
        flash('Service updated successfully!', 'success')
        return redirect(url_for('admin_services'))
    return render_template('edit_service.html', service=service)



@app.route('/admin/service/delete/<int:service_id>', methods=['POST'])
@login_required
def delete_service(service_id):
    if current_user.role != 'admin':
        flash('You do not have permission to delete this service.', 'danger')
        return redirect(url_for('admin_services'))
    service = Service.query.get_or_404(service_id)
    db.session.delete(service)
    db.session.commit()
    flash('Service deleted successfully!', 'success')
    return redirect(url_for('admin_services'))



@app.route('/admin/unblock_user/<int:user_id>', methods=['POST'])
@login_required
def unblock_user(user_id):
    if current_user.role != 'admin':
        flash('You are not authorized to access this page.', 'danger')
        return redirect(url_for('login'))
    user = db.session.get(User, user_id)
    if user and user.role != 'admin': 
        user.status = 'pending' 
        db.session.commit()
        flash(f'User {user.username} has been unblocked.', 'success')
    else:
        flash('User not found or invalid operation.', 'danger')
    return redirect(url_for('admin_dashboard'))



@app.route('/verify_profile/<int:user_id>', methods=['POST'])
@login_required
def verify_profile(user_id):
    if current_user.role != 'admin':
        flash('You are not authorized to verify profiles.', 'danger')
        return redirect(url_for('login'))
    user = User.query.get(user_id)
    if user and user.role == 'professional':
        user.profile_verified = True
        db.session.commit()
        flash(f"Profile of '{user.username}' has been verified.", "success")
    else:
        flash("User not found or invalid operation.", "danger")
    return redirect(url_for('admin_dashboard'))



@app.route('/customer/dashboard')
@login_required
@check_user_status
def customer_dashboard():
    if current_user.role != 'customer':
        flash('You are not authorized to access this page.', 'danger')
        return redirect(url_for('login'))
    service_requests = ServiceRequest.query.filter_by(customer_id=current_user.id).all()
    return render_template('customer_dashboard.html', service_requests=service_requests)



@app.route('/customer/request_service', methods=['GET', 'POST'])
@login_required
def request_service():
    form = ServiceRequestForm()
    form.service_id.choices = [(service.id, service.name) for service in Service.query.all()]
    if form.validate_on_submit():
        try:
            service_request = ServiceRequest(
                customer_id=current_user.id,
                service_id=form.service_id.data,
                location=form.location.data,
                remarks=form.remarks.data,
                status='pending', 
                professional_id=None  
            )
            db.session.add(service_request)
            db.session.commit()
            flash('Service request submitted successfully!', 'success')
            return redirect(url_for('customer_dashboard'))
        except Exception as e:
            db.session.rollback() 
            print("Error committing to the database:", e)
            flash("An error occurred while processing your request.", "danger")
            return redirect(url_for('request_service'))
    return render_template('request_service.html', form=form)



@app.route('/customer/service/<int:service_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_customer_service(service_id):
    if current_user.role != 'customer':
        flash('You are not authorized to access this page.', 'danger')
        return redirect(url_for('login'))
    service_request = ServiceRequest.query.get_or_404(service_id)
    if service_request.customer_id != current_user.id:
        flash('You are not authorized to modify this service request.', 'danger')
        return redirect(url_for('customer_dashboard'))
    if request.method == 'POST':
        service_request.remarks = request.form.get('remarks', service_request.remarks)
        service_request.status = request.form.get('status', service_request.status)
        if service_request.status == 'completed':
            service_request.review = request.form.get('review')
            try:
                service_request.rating = int(request.form.get('rating'))
                if not (1 <= service_request.rating <= 5):
                    raise ValueError("Invalid rating")
            except (ValueError, TypeError):
                flash("Rating must be a number between 1 and 5.", "danger")
                return render_template('edit_customer_service.html', service_request=service_request)
        db.session.commit()
        flash('Service request updated successfully!', 'success')
        return redirect(url_for('customer_dashboard'))
    return render_template('edit_customer_service.html', service_request=service_request)



@app.route('/customer/services')
@login_required
def list_services():
    services = Service.query.all()
    print("Services available:", services) 
    return render_template('list_services.html', services=services)



@app.route('/professional/dashboard')
@login_required
def professional_dashboard():
    if current_user.role != 'professional':
        flash('You are not authorized to access this page.', 'danger')
        return redirect(url_for('login'))
    if current_user.status != 'approved':
        flash('Your account is awaiting admin approval.', 'warning')
        return redirect(url_for('login'))
    assigned_requests = ServiceRequest.query.filter_by(professional_id=current_user.id).all()
    unclaimed_requests = ServiceRequest.query.filter(
        ServiceRequest.professional_id == None, 
        ServiceRequest.status == 'pending' 
    ).all()
    return render_template(
        'professional_dashboard.html',
        assigned_requests=assigned_requests,
        unclaimed_requests=unclaimed_requests
    )




@app.route('/claim_request/<int:request_id>', methods=['POST'])
@login_required
def claim_request(request_id):
    if current_user.role != 'professional':
        flash('You are not authorized to claim this service request.', 'danger')
        return redirect(url_for('login'))
    if current_user.status != 'approved':
        flash('Your account must be approved by the admin to claim requests.', 'danger')
        return redirect(url_for('professional_dashboard'))
    service_request = ServiceRequest.query.get_or_404(request_id)
    if service_request.professional_id is not None:
        flash('This service request has already been claimed by another professional.', 'warning')
        return redirect(url_for('professional_dashboard'))
    if service_request.status != 'pending':
        flash('This service request cannot be claimed at the moment.', 'warning')
        return redirect(url_for('professional_dashboard'))
    service_request.professional_id = current_user.id
    service_request.status = 'in_progress' 
    db.session.commit()
    flash('Service request successfully claimed.', 'success')
    return redirect(url_for('professional_dashboard'))




@app.route('/update_request_status/<int:request_id>/<string:status>', methods=['POST'])
@login_required
def update_request_status(request_id, status):
    if current_user.role != 'professional':
        flash('You are not authorized to update service requests.', 'danger')
        return redirect(url_for('login'))
    if current_user.status != 'approved':
        flash('Your account must be approved by the admin to perform this action.', 'danger')
        return redirect(url_for('professional_dashboard'))
    service_request = ServiceRequest.query.get_or_404(request_id)
    if service_request.professional_id != current_user.id:
        flash('You can only update service requests assigned to you.', 'warning')
        return redirect(url_for('professional_dashboard'))
    valid_statuses = ['claimed', 'in_progress', 'completed']
    if status in valid_statuses:
        service_request.status = status
        db.session.commit()
        flash(f'Service request status updated to "{status}".', 'success')
    else:
        flash('Invalid status update.', 'danger')
    return redirect(url_for('professional_dashboard'))



@app.route('/professional/complete_request/<int:request_id>', methods=['POST'])
@login_required
@check_user_status
def complete_request(request_id):
    if current_user.role != 'professional':
        flash('You are not authorized to access this page.', 'danger')
        return redirect(url_for('login'))
    request = ServiceRequest.query.get(request_id)
    if request and request.professional_id == current_user.id:
        request.status = 'completed' 
        db.session.commit()
        flash('Service request marked as completed.', 'success')
    else:
        flash('You are not authorized to complete this request.', 'danger')
    return redirect(url_for('professional_dashboard'))



@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, render_template, redirect, url_for, request, session, flash
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId






app = Flask(__name__)
app.secret_key = 'super_secret_key'  # Change this for production

# MongoDB Connection
client = MongoClient('mongodb://localhost:27017/doctor_appointment_system')
db = client['doctor_appointment_system']
users_collection = db['users']
appointments_collection = db['appointments']
doctors_collection = db['doctors']

# ✅ Home Page
@app.route('/')
def index():
    return render_template('index.html')

# ✅ Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = users_collection.find_one({'email': email})

        if user and check_password_hash(user['password'], password):
            session['user'] = user['name']
            session['role'] = user['role']
            return redirect(url_for('admin_dashboard' if user['role'] == 'admin' else 'user_dashboard'))
        else:
            flash('Invalid email or password', 'error')

    return render_template('login.html')

# ✅ Registration Page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = generate_password_hash(request.form['password'], method='pbkdf2:sha256')
        role = request.form['role']

        if users_collection.find_one({'email': email}):
            flash('Email already exists! Please log in.', 'error')
            return redirect(url_for('login'))

        users_collection.insert_one({'name': name, 'email': email, 'password': password, 'role': role})
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

# ✅ Admin Dashboard
@app.route('/admin')
def admin_dashboard():
    if 'user' in session and session.get('role') == 'admin':
        return render_template('admin_dashboard.html')
    return redirect(url_for('login'))

# ✅ User Dashboard
@app.route('/user')
def user_dashboard():
    if 'user' in session and session.get('role') == 'user':
        user_appointments = appointments_collection.find({'patient_name': session['user']})
        return render_template('user_dashboard.html', appointments=user_appointments)
    return redirect(url_for('login'))

# ✅ Add Doctor (Admin)
@app.route('/add_doctor', methods=['GET', 'POST'])
def add_doctor():
    if 'user' in session and session.get('role') == 'admin':
        if request.method == 'POST':
            name = request.form['name']
            specialization = request.form['specialization']

            doctors_collection.insert_one({
                'name': name,
                'specialization': specialization
            })

            flash('Doctor successfully added.', 'success')
            return redirect(url_for('admin_dashboard'))

        return render_template('add_doctor.html')
    
    return redirect(url_for('login'))

# ✅ Request Appointment (User)
@app.route('/request_appointment', methods=['GET', 'POST'])
def request_appointment():
    if 'user' in session and session.get('role') == 'user':
        if request.method == 'POST':
            doctor_id = request.form['doctor_id']
            appointment_time = request.form['appointment_time']
            doctor = doctors_collection.find_one({'_id': ObjectId(doctor_id)})

            if doctor:
                appointments_collection.insert_one({
                    'doctor_name': doctor['name'],
                    'patient_name': session['user'],
                    'appointment_time': appointment_time
                })
                flash('Appointment request successful!', 'success')
                return redirect(url_for('user_dashboard'))

        doctors = doctors_collection.find({})
        return render_template('request_appointment.html', doctors=doctors)

    return redirect(url_for('login'))

# ✅ Manage Appointments (Admin)
@app.route('/manage_appointments', methods=['GET', 'POST'])
def manage_appointments():
    if 'user' in session and session.get('role') == 'admin':
        if request.method == 'POST':
            doctor_name = request.form['doctor_name']
            patient_name = request.form['patient_name']
            appointment_time = request.form['appointment_time']

            appointments_collection.insert_one({
                'doctor_name': doctor_name,
                'patient_name': patient_name,
                'appointment_time': appointment_time
            })

            flash('Appointment successfully added.', 'success')
            return redirect(url_for('manage_appointments'))

        doctors = doctors_collection.find({})
        return render_template('manage_appointments.html', doctors=doctors)

    return redirect(url_for('login'))

# ✅ View Appointments (Admin)
@app.route('/view_appointments')
def view_appointments():
    if 'user' in session and session.get('role') == 'admin':
        appointments = appointments_collection.find({})
        return render_template('view_appointments.html', appointments=appointments)
    return redirect(url_for('login'))

# ✅ Update Appointment (Admin)
@app.route('/update_appointment/<appointment_id>', methods=['GET', 'POST'])
def update_appointment(appointment_id):
    if 'user' in session and session.get('role') == 'admin':
        if request.method == 'POST':
            doctor_name = request.form['doctor_name']
            patient_name = request.form['patient_name']
            appointment_time = request.form['appointment_time']

            appointments_collection.update_one(
                {'_id': ObjectId(appointment_id)},
                {'$set': {
                    'doctor_name': doctor_name,
                    'patient_name': patient_name,
                    'appointment_time': appointment_time
                }}
            )
            flash('Appointment successfully updated.', 'success')
            return redirect(url_for('view_appointments'))

        appointment = appointments_collection.find_one({'_id': ObjectId(appointment_id)})
        doctors = doctors_collection.find()
        return render_template('update_appointment.html', appointment=appointment, doctors=doctors)

    return redirect(url_for('login'))

# ✅ Delete Appointment (Admin)
@app.route('/delete_appointment/<appointment_id>')
def delete_appointment(appointment_id):
    if 'user' in session and session.get('role') == 'admin':
        appointments_collection.delete_one({'_id': ObjectId(appointment_id)})
        flash('Appointment successfully deleted.', 'success')
        return redirect(url_for('view_appointments'))

    return redirect(url_for('login'))

# ✅ Logout
@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

# ✅ Run Flask App
if __name__ == '__main__':
    app.run(debug=True)






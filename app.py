from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3

app = Flask(__name__, template_folder='.')
app.secret_key = 'petcare_secure_secret_key_999'

def get_db_connection():
    conn = sqlite3.connect('petcare.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    services = conn.execute('SELECT * FROM Service_Catalog').fetchall()
    conn.close()
    return render_template('index.html', services=services)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')
        
        conn = get_db_connection()
        if role == 'owner':
            user = conn.execute('SELECT * FROM Owner WHERE email = ? AND password = ?', (email, password)).fetchone()
            if user:
                session['user_id'] = user['owner_id']
                session['role'] = 'owner'
                conn.close()
                return redirect(url_for('dashboard_owner', owner_id=user['owner_id']))
        else:
            user = conn.execute('SELECT * FROM Service_Provider WHERE email = ? AND password = ?', (email, password)).fetchone()
            if user:
                session['user_id'] = user['provider_id']
                session['role'] = 'provider'
                conn.close()
                return redirect(url_for('provider_dashboard'))
        conn.close()
        flash('Invalid email, password, or role. Please try again.', 'danger')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        password = request.form.get('password')
        role = request.form.get('role')
        
        conn = get_db_connection()
        try:
            if role == 'owner':
                conn.execute('INSERT INTO Owner (full_name, email, phone, password) VALUES (?, ?, ?, ?)',
                             (full_name, email, phone, password))
            else:
                clinic_name = request.form.get('clinic_name', 'Independent Practice')
                provider_role = request.form.get('provider_role', 'Veterinarian')
                exp_years = int(request.form.get('experience_years', 3))
                qualification = request.form.get('qualification', 'Certified Professional')
                conn.execute('''
                    INSERT INTO Service_Provider (full_name, email, phone, role, clinic_or_shop_name, experience_years, qualification, password)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (full_name, email, phone, provider_role, clinic_name, exp_years, qualification, password))
            conn.commit()
            conn.close()
            flash('Registration successful! Please sign in.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            conn.close()
            flash(f'Registration error (Email may already exist): {str(e)}', 'danger')
    return render_template('register.html')

@app.route('/dashboard')
@app.route('/dashboard/<int:owner_id>')
def dashboard_owner(owner_id=None):
    if owner_id is None:
        owner_id = session.get('user_id') or 1
    conn = get_db_connection()
    owner = conn.execute('SELECT * FROM Owner WHERE owner_id = ?', (owner_id,)).fetchone()
    if not owner:
        owner = {'owner_id': owner_id, 'full_name': 'Alex Turner', 'email': 'owner@test.com'}
    pets = conn.execute('SELECT * FROM Pet WHERE owner_id = ?', (owner_id,)).fetchall()
    bookings = conn.execute('''
        SELECT b.*, p.name AS pet_name, sp.full_name AS provider_name, sp.role AS provider_role, sc.service_name, sc.base_price
        FROM Booking b
        JOIN Pet p ON b.pet_id = p.pet_id
        JOIN Service_Provider sp ON b.provider_id = sp.provider_id
        JOIN Service_Catalog sc ON b.service_id = sc.service_id
        WHERE b.owner_id = ?
    ''', (owner_id,)).fetchall()
    conn.close()
    return render_template('dashboard.html', owner=owner, pets=pets, bookings=bookings)

@app.route('/provider-dashboard')
def provider_dashboard():
    provider_id = session.get('user_id') or 2
    conn = get_db_connection()
    provider = conn.execute('SELECT * FROM Service_Provider WHERE provider_id = ?', (provider_id,)).fetchone()
    if not provider:
        provider = {'provider_id': provider_id, 'full_name': 'Dr. Sarah Jenkins', 'role': 'Veterinarian', 'email': 'vet@test.com', 'clinic_or_shop_name': 'Paws Clinic', 'experience_years': 8, 'qualification': 'BVSc & AH'}
    bookings = conn.execute('''
        SELECT b.*, p.name AS pet_name, o.full_name AS owner_name, o.phone AS owner_phone, sc.service_name, sc.base_price
        FROM Booking b
        JOIN Pet p ON b.pet_id = p.pet_id
        JOIN Owner o ON b.owner_id = o.owner_id
        JOIN Service_Catalog sc ON b.service_id = sc.service_id
        WHERE b.provider_id = ?
    ''', (provider_id,)).fetchall()
    conn.close()
    return render_template('provider_dashboard.html', provider=provider, bookings=bookings)

@app.route('/book', methods=['GET', 'POST'])
@app.route('/book/<int:owner_id>', methods=['GET', 'POST'])
def book_service(owner_id=None):
    if owner_id is None:
        owner_id = session.get('user_id') or 1
    conn = get_db_connection()
    if request.method == 'POST':
        pet_id = request.form.get('pet_id')
        service_id = request.form.get('service_id')
        provider_id = request.form.get('provider_id')
        booking_date = request.form.get('booking_date')
        booking_time = request.form.get('booking_time')
        
        conn.execute('''
            INSERT INTO Booking (owner_id, pet_id, service_id, provider_id, booking_date, booking_time, status)
            VALUES (?, ?, ?, ?, ?, ?, 'Confirmed')
        ''', (owner_id, pet_id, service_id, provider_id, booking_date, booking_time))
        conn.commit()
        conn.close()
        flash('Appointment booked successfully! 🐾', 'success')
        return redirect(url_for('dashboard_owner', owner_id=owner_id))
        
    pets = conn.execute('SELECT * FROM Pet WHERE owner_id = ?', (owner_id,)).fetchall()
    services = conn.execute('SELECT * FROM Service_Catalog').fetchall()
    providers = conn.execute('SELECT * FROM Service_Provider').fetchall()
    conn.close()
    return render_template('book.html', owner_id=owner_id, pets=pets, services=services, providers=providers)

@app.route('/reschedule/<int:booking_id>', methods=['GET', 'POST'])
def reschedule_booking(booking_id):
    conn = get_db_connection()
    if request.method == 'POST':
        new_date = request.form.get('booking_date')
        new_time = request.form.get('booking_time')
        conn.execute('UPDATE Booking SET booking_date = ?, booking_time = ? WHERE booking_id = ?', (new_date, new_time, booking_id))
        conn.commit()
        conn.close()
        flash('Appointment rescheduled successfully!', 'success')
        return redirect(url_for('dashboard_owner'))
    
    booking = conn.execute('''
        SELECT b.*, p.name AS pet_name, sp.full_name AS provider_name, sc.service_name
        FROM Booking b
        JOIN Pet p ON b.pet_id = p.pet_id
        JOIN Service_Provider sp ON b.provider_id = sp.provider_id
        JOIN Service_Catalog sc ON b.service_id = sc.service_id
        WHERE b.booking_id = ?
    ''', (booking_id,)).fetchone()
    conn.close()
    return render_template('reschedule.html', booking=booking)

@app.route('/cancel-booking/<int:booking_id>', methods=['POST'])
def cancel_booking(booking_id):
    conn = get_db_connection()
    conn.execute("UPDATE Booking SET status = 'Cancelled' WHERE booking_id = ?", (booking_id,))
    conn.commit()
    conn.close()
    flash('Appointment cancelled.', 'warning')
    return redirect(request.referrer or url_for('dashboard_owner'))

@app.route('/complete-booking/<int:booking_id>', methods=['POST'])
@app.route('/complete/<int:booking_id>', methods=['POST'])
def complete_booking(booking_id):
    conn = get_db_connection()
    conn.execute("UPDATE Booking SET status = 'Completed' WHERE booking_id = ?", (booking_id,))
    conn.commit()
    conn.close()
    flash('Appointment marked as completed! 🐾', 'success')
    return redirect(url_for('provider_dashboard'))

@app.route('/medical-records/<int:pet_id>')
def medical_records(pet_id):
    conn = get_db_connection()
    pet = conn.execute('SELECT p.*, o.full_name AS owner_name FROM Pet p JOIN Owner o ON p.owner_id = o.owner_id WHERE p.pet_id = ?', (pet_id,)).fetchone()
    records = conn.execute('SELECT * FROM Medical_Record WHERE pet_id = ?', (pet_id,)).fetchall()
    conn.close()
    return render_template('medical_records.html', pet=pet, records=records)

@app.route('/add-medical-record/<int:pet_id>', methods=['POST'])
def add_medical_record(pet_id):
    diagnosis = request.form.get('diagnosis')
    treatment = request.form.get('treatment')
    author = session.get('role', 'owner').capitalize()
    conn = get_db_connection()
    conn.execute('INSERT INTO Medical_Record (pet_id, author_name, diagnosis, treatment) VALUES (?, ?, ?, ?)', (pet_id, author, diagnosis, treatment))
    conn.commit()
    conn.close()
    flash('Clinical record saved successfully.', 'success')
    return redirect(url_for('medical_records', pet_id=pet_id))

@app.route('/add-provider-record', methods=['POST'])
def add_provider_record():
    pet_identifier = request.form.get('pet_identifier')
    diagnosis = request.form.get('diagnosis')
    treatment = request.form.get('treatment')
    provider_id = session.get('user_id') or 2
    
    conn = get_db_connection()
    provider = conn.execute('SELECT full_name FROM Service_Provider WHERE provider_id = ?', (provider_id,)).fetchone()
    author_name = provider['full_name'] if provider else 'Provider'
    
    pet = conn.execute('SELECT pet_id FROM Pet WHERE pet_id = ? OR name LIKE ?', (pet_identifier, f"%{pet_identifier}%")).fetchone()
    if pet:
        conn.execute('INSERT INTO Medical_Record (pet_id, provider_id, author_name, diagnosis, treatment) VALUES (?, ?, ?, ?, ?)',
                     (pet['pet_id'], provider_id, author_name, diagnosis, treatment))
        conn.commit()
        flash('Pet record and feedback saved successfully!', 'success')
    else:
        flash('Pet not found. Please enter a valid pet name or ID.', 'danger')
    conn.close()
    return redirect(url_for('provider_dashboard'))

@app.route('/add-pet', methods=['POST'])
def add_pet():
    owner_id = session.get('user_id') or 1
    name = request.form.get('name')
    species = request.form.get('species')
    breed = request.form.get('breed')
    try:
        age = int(request.form.get('age', 1))
        if age <= 0:
            raise ValueError()
    except ValueError:
        flash('Pet age must be greater than 0!', 'danger')
        return redirect(url_for('dashboard_owner', owner_id=owner_id))
        
    gender = request.form.get('gender')
    
    conn = get_db_connection()
    conn.execute('INSERT INTO Pet (owner_id, name, species, breed, age, gender) VALUES (?, ?, ?, ?, ?, ?)',
                 (owner_id, name, species, breed, age, gender))
    conn.commit()
    conn.close()
    flash('New pet companion registered successfully! 🐾', 'success')
    return redirect(url_for('dashboard_owner', owner_id=owner_id))

@app.route('/review/<int:booking_id>', methods=['GET', 'POST'])
def review(booking_id):
    conn = get_db_connection()
    if request.method == 'POST':
        flash('Review and feedback submitted successfully!', 'success')
        conn.close()
        return redirect(url_for('dashboard_owner'))
    booking = conn.execute('SELECT b.*, sc.service_name, sp.full_name AS provider_name FROM Booking b JOIN Service_Catalog sc ON b.service_id = sc.service_id JOIN Service_Provider sp ON b.provider_id = sp.provider_id WHERE b.booking_id = ?', (booking_id,)).fetchone()
    conn.close()
    return render_template('review.html', booking=booking)

@app.route('/data-flow')
def data_flow():
    conn = sqlite3.connect('petcare.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Fetch data for Interconnections (Section 2)
    interconnections = cursor.execute('''
        SELECT p.name AS pet_name, o.full_name AS owner_name, 
               sp.full_name AS provider_name, s.service_name
        FROM Pet p
        JOIN Owner o ON p.owner_id = o.owner_id
        LEFT JOIN Booking b ON p.pet_id = b.pet_id
        LEFT JOIN Service_Catalog s ON b.service_id = s.service_id
        LEFT JOIN Service_Provider sp ON b.provider_id = sp.provider_id
    ''').fetchall()
    
    # Fetch data for Appointments (Section 3)
    appointments = cursor.execute('''
        SELECT p.name AS pet_name, s.service_name, b.status
        FROM Booking b
        JOIN Pet p ON b.pet_id = p.pet_id
        JOIN Service_Catalog s ON b.service_id = s.service_id
    ''').fetchall()
    
    conn.close()
    return render_template('data_flow.html', interconnections=interconnections, appointments=appointments)

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('login'))

import os
from reset_and_seed_all import rebuild_database

if not os.path.exists('petcare.db'):
    rebuild_database()

if __name__ == '__main__':
    app.run(debug=True)

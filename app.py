import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__, template_folder='.')
app.secret_key = 'supersecretpetcarekey'

def get_db_connection():
    conn = sqlite3.connect('petcare.db', timeout=20)
    conn.row_factory = sqlite3.Row
    conn.execute('PRAGMA journal_mode=WAL;')
    return conn

# 1. Home Page / Service Catalog
@app.route('/')
def home():
    conn = get_db_connection()
    services = conn.execute("SELECT * FROM Service_Catalog").fetchall()
    conn.close()
    return render_template('index.html', services=services)

# 2. Register Owner
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        full_name = request.form['full_name']
        email = request.form['email']
        password = request.form['password']
        phone = request.form.get('phone', '')
        address = request.form.get('address', '')

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Owner (full_name, email, password, phone, address)
            VALUES (?, ?, ?, ?, ?)
        """, (full_name, email, password, phone, address))
        owner_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return redirect(url_for('dashboard', owner_id=owner_id))

    return render_template('register.html')
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Owner WHERE email = ? AND password = ?", (email, password))
        owner = cursor.fetchone()
        conn.close()

        if owner:
            session['owner_id'] = owner['owner_id'] if 'owner_id' in owner.keys() else owner[0]
            session['owner_name'] = owner['full_name'] if 'full_name' in owner.keys() else owner[1]
            return redirect('/dashboard')
        else:
            return "Invalid email or password. <a href='/login'>Try again</a>", 401

    return render_template('login.html')

# 3. Owner Dashboard
@app.route('/dashboard/<int:owner_id>')
def dashboard(owner_id):
    conn = get_db_connection()
    owner = conn.execute("SELECT * FROM Owner WHERE owner_id = ?", (owner_id,)).fetchone()
    pets = conn.execute("SELECT * FROM Pet WHERE owner_id = ?", (owner_id,)).fetchall()
    bookings = conn.execute("""
        SELECT 
            b.booking_id,
            b.booking_date,
            b.booking_time,
            b.status,
            p.name AS pet_name,
            s.service_name,
            sp.full_name AS provider_name
        FROM Booking b
        JOIN Pet p ON b.pet_id = p.pet_id
        JOIN Service_Catalog s ON b.service_id = s.service_id
        JOIN Service_Provider sp ON b.provider_id = sp.provider_id
        WHERE b.owner_id = ?
        ORDER BY b.booking_date DESC
    """, (owner_id,)).fetchall()
    conn.close()
    return render_template('dashboard.html', owner=owner, pets=pets, bookings=bookings)

# 4. Add Pet
@app.route('/add-pet/<int:owner_id>', methods=['POST'])
def add_pet(owner_id):
    name = request.form['name']
    species = request.form['species']
    breed = request.form.get('breed', '')
    age = request.form.get('age', None)
    gender = request.form.get('gender', '')

    conn = get_db_connection()
    conn.execute("""
        INSERT INTO Pet (owner_id, name, species, breed, age, gender)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (owner_id, name, species, breed, age, gender))
    conn.commit()
    conn.close()
    return redirect(url_for('dashboard', owner_id=owner_id))

# 5. Book an Appointment
@app.route('/book/<int:owner_id>', methods=['GET', 'POST'])
def book_service(owner_id):
    conn = get_db_connection()

    if request.method == 'POST':
        pet_id = request.form['pet_id']
        service_id = request.form['service_id']
        provider_id = request.form['provider_id']
        booking_date = request.form['booking_date']
        booking_time = request.form['booking_time']

        conn.execute("""
            INSERT INTO Booking (owner_id, pet_id, provider_id, service_id, booking_date, booking_time, status)
            VALUES (?, ?, ?, ?, ?, ?, 'Confirmed')
        """, (owner_id, pet_id, provider_id, service_id, booking_date, booking_time))
        conn.commit()
        conn.close()
        return redirect(url_for('dashboard', owner_id=owner_id))

    pets = conn.execute("SELECT * FROM Pet WHERE owner_id = ?", (owner_id,)).fetchall()
    services = conn.execute("SELECT * FROM Service_Catalog").fetchall()
    providers = conn.execute("SELECT * FROM Service_Provider").fetchall()
    conn.close()

    return render_template('book.html', owner_id=owner_id, pets=pets, services=services, providers=providers)

# 6. Medical Records (View & Add)
@app.route('/medical-records/<int:pet_id>', methods=['GET', 'POST'])
def medical_records(pet_id):
    conn = get_db_connection()

    if request.method == 'POST':
        provider_id = request.form['provider_id']
        treatment_name = request.form['treatment_name']
        date_administered = request.form['date_administered']
        next_due_date = request.form.get('next_due_date', None)
        notes = request.form.get('notes', '')

        conn.execute("""
            INSERT INTO Medical_Record (pet_id, provider_id, treatment_name, date_administered, next_due_date, notes)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (pet_id, provider_id, treatment_name, date_administered, next_due_date, notes))
        conn.commit()
        conn.close()
        return redirect(url_for('medical_records', pet_id=pet_id))

    pet = conn.execute("SELECT * FROM Pet WHERE pet_id = ?", (pet_id,)).fetchone()
    providers = conn.execute("SELECT * FROM Service_Provider").fetchall()
    records = conn.execute("""
        SELECT m.*, sp.full_name AS provider_name
        FROM Medical_Record m
        LEFT JOIN Service_Provider sp ON m.provider_id = sp.provider_id
        WHERE m.pet_id = ? 
        ORDER BY m.date_administered DESC
    """, (pet_id,)).fetchall()
    conn.close()

    return render_template('medical_records.html', pet=pet, providers=providers, records=records)
# 7. Add Review
@app.route('/review/<int:booking_id>', methods=['GET', 'POST'])
def review(booking_id):
    conn = get_db_connection()

    # Get booking details to pre-populate review info
    booking = conn.execute("""
        SELECT 
            b.booking_id,
            b.owner_id,
            b.provider_id,
            b.booking_date,
            p.name AS pet_name,
            s.service_name,
            sp.full_name AS provider_name
        FROM Booking b
        JOIN Pet p ON b.pet_id = p.pet_id
        JOIN Service_Catalog s ON b.service_id = s.service_id
        JOIN Service_Provider sp ON b.provider_id = sp.provider_id
        WHERE b.booking_id = ?
    """, (booking_id,)).fetchone()

    if request.method == 'POST':
        rating = request.form['rating']
        comment = request.form.get('comment', '')
        review_date = request.form['review_date']

        conn.execute("""
            INSERT INTO Review (booking_id, owner_id, provider_id, rating, comment, review_date)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (booking_id, booking['owner_id'], booking['provider_id'], rating, comment, review_date))
        conn.commit()
        conn.close()
        return redirect(url_for('dashboard', owner_id=booking['owner_id']))

    # Check if a review already exists for this booking
    existing_review = conn.execute("SELECT * FROM Review WHERE booking_id = ?", (booking_id,)).fetchone()
    conn.close()

    return render_template('review.html', booking=booking, existing_review=existing_review)
if __name__ == '__main__':
    app.run(debug=True)

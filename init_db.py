import sqlite3

def create_database():
    conn = sqlite3.connect("petcare.db")
    cursor = conn.cursor()

    # Enable foreign keys
    cursor.execute("PRAGMA foreign_keys = ON;")

    # 1. Owner Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Owner (
        owner_id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        phone TEXT NOT NULL,
        address TEXT NOT NULL,
        password TEXT NOT NULL
    );
    """)

    # 2. Pet Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Pet (
        pet_id INTEGER PRIMARY KEY AUTOINCREMENT,
        owner_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        species TEXT NOT NULL,
        breed TEXT,
        age INTEGER,
        gender TEXT,
        FOREIGN KEY (owner_id) REFERENCES Owner(owner_id) ON DELETE CASCADE
    );
    """)

    # 3. Service Provider Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Service_Provider (
        provider_id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT NOT NULL,
        role TEXT NOT NULL,
        phone TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        clinic_or_shop_name TEXT,
        experience_years INTEGER
    );
    """)

    # 4. Service Catalog Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Service_Catalog (
        service_id INTEGER PRIMARY KEY AUTOINCREMENT,
        service_name TEXT NOT NULL,
        category TEXT NOT NULL,
        base_price REAL NOT NULL,
        duration_minutes INTEGER NOT NULL
    );
    """)

    # 5. Booking Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Booking (
        booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
        owner_id INTEGER NOT NULL,
        pet_id INTEGER NOT NULL,
        provider_id INTEGER NOT NULL,
        service_id INTEGER NOT NULL,
        booking_date TEXT NOT NULL,
        booking_time TEXT NOT NULL,
        status TEXT DEFAULT 'Pending',
        FOREIGN KEY (owner_id) REFERENCES Owner(owner_id),
        FOREIGN KEY (pet_id) REFERENCES Pet(pet_id),
        FOREIGN KEY (provider_id) REFERENCES Service_Provider(provider_id),
        FOREIGN KEY (service_id) REFERENCES Service_Catalog(service_id)
    );
    """)

    # 6. Medical Record Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Medical_Record (
        record_id INTEGER PRIMARY KEY AUTOINCREMENT,
        pet_id INTEGER NOT NULL,
        provider_id INTEGER NOT NULL,
        treatment_name TEXT NOT NULL,
        date_administered TEXT NOT NULL,
        next_due_date TEXT,
        notes TEXT,
        FOREIGN KEY (pet_id) REFERENCES Pet(pet_id),
        FOREIGN KEY (provider_id) REFERENCES Service_Provider(provider_id)
    );
    """)

    # 7. Payment Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Payment (
        payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
        booking_id INTEGER NOT NULL,
        amount REAL NOT NULL,
        payment_method TEXT NOT NULL,
        payment_status TEXT DEFAULT 'Paid',
        payment_date TEXT NOT NULL,
        FOREIGN KEY (booking_id) REFERENCES Booking(booking_id)
    );
    """)

    # 8. Review Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Review (
        review_id INTEGER PRIMARY KEY AUTOINCREMENT,
        booking_id INTEGER NOT NULL,
        owner_id INTEGER NOT NULL,
        provider_id INTEGER NOT NULL,
        rating INTEGER CHECK(rating >= 1 AND rating <= 5),
        comment TEXT,
        review_date TEXT NOT NULL,
        FOREIGN KEY (booking_id) REFERENCES Booking(booking_id),
        FOREIGN KEY (owner_id) REFERENCES Owner(owner_id),
        FOREIGN KEY (provider_id) REFERENCES Service_Provider(provider_id)
    );
    """)

    # Insert initial catalog data
    cursor.execute("""
    INSERT OR IGNORE INTO Service_Catalog (service_id, service_name, category, base_price, duration_minutes)
    VALUES 
    (1, 'Full Grooming Bath & Haircut', 'Grooming', 45.0, 60),
    (2, 'Nail Trim & Ear Cleaning', 'Grooming', 20.0, 30),
    (3, 'Rabies Vaccination', 'Veterinary', 35.0, 15),
    (4, 'General Health Checkup', 'Veterinary', 50.0, 30),
    (5, 'Overnight Pet Boarding', 'Boarding', 40.0, 1440);
    """)

    conn.commit()
    conn.close()
    print("Database created and initialized successfully!")

if __name__ == "__main__":
    create_database()
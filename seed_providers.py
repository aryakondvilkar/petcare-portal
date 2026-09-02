import sqlite3

conn = sqlite3.connect("petcare.db")
cursor = conn.cursor()

# Insert dummy veterinarians and groomers
providers = [
    ('Dr. Aditi Sharma', 'Veterinarian', '9876543210', 'aditi@petclinic.com', 'Happy Paws Clinic'),
    ('Dr. Rohan Verma', 'Veterinarian', '9876543211', 'rohan@vetcare.com', 'City Pet Hospital'),
    ('Pooja Nair', 'Groomer', '9876543212', 'pooja@grooming.com', 'Paws & Bubbles Salon'),
    ('Amit Patel', 'Trainer', '9876543213', 'amit@k9training.com', 'Alpha Dog Academy')
]

cursor.executemany("""
    INSERT OR IGNORE INTO Service_Provider (full_name, role, phone, email, clinic_or_shop_name)
    VALUES (?, ?, ?, ?, ?)
""", providers)

conn.commit()
conn.close()

print("Service providers inserted successfully!")
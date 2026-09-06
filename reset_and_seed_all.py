import sqlite3
import os

db_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'petcare.db')

def rebuild_database():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.executescript('''
        DROP TABLE IF EXISTS Booking;
        DROP TABLE IF EXISTS Medical_Record;
        DROP TABLE IF EXISTS Pet;
        DROP TABLE IF EXISTS Service_Catalog;
        DROP TABLE IF EXISTS Service_Provider;
        DROP TABLE IF EXISTS Owner;

        CREATE TABLE Owner (
            owner_id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT,
            password TEXT NOT NULL
        );

        CREATE TABLE Service_Provider (
            provider_id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            role TEXT NOT NULL,
            phone TEXT,
            email TEXT UNIQUE NOT NULL,
            clinic_or_shop_name TEXT,
            experience_years INTEGER,
            qualification TEXT,
            password TEXT DEFAULT '1234'
        );

        CREATE TABLE Service_Catalog (
            service_id INTEGER PRIMARY KEY AUTOINCREMENT,
            service_name TEXT NOT NULL,
            base_price DECIMAL,
            description TEXT,
            category TEXT,
            image_url TEXT
        );

        CREATE TABLE Pet (
            pet_id INTEGER PRIMARY KEY AUTOINCREMENT,
            owner_id INTEGER,
            name TEXT NOT NULL,
            species TEXT,
            breed TEXT,
            age INTEGER,
            gender TEXT,
            FOREIGN KEY (owner_id) REFERENCES Owner(owner_id)
        );

        CREATE TABLE Booking (
            booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
            owner_id INTEGER,
            pet_id INTEGER,
            service_id INTEGER,
            provider_id INTEGER,
            booking_date TEXT,
            booking_time TEXT,
            status TEXT,
            FOREIGN KEY (owner_id) REFERENCES Owner(owner_id),
            FOREIGN KEY (pet_id) REFERENCES Pet(pet_id),
            FOREIGN KEY (service_id) REFERENCES Service_Catalog(service_id),
            FOREIGN KEY (provider_id) REFERENCES Service_Provider(provider_id)
        );
    ''')

    # Owners matching exact quick demo buttons
    owners = [
        ("Alex Turner", "alex@test.com", "9876543210", "1234"),
        ("Priya Sharma", "priya@example.com", "9123456789", "1234"),
        ("David Miller", "david@example.com", "9811223344", "1234"),
        ("Ananya Roy", "ananya@example.com", "9722334455", "1234"),
        ("Carlos Gomez", "carlos@example.com", "9633445566", "1234"),
        ("Sarah Jenkins", "sarah@example.com", "555-0101", "1234"),
        ("Michael Chang", "michael@example.com", "555-0102", "1234"),
        ("Emily Blunt", "emily@example.com", "555-0103", "1234"),
        ("Jessica Alba", "jessica@example.com", "555-0104", "1234"),
        ("Robert Downey", "robert@example.com", "555-0105", "1234")
    ]
    cursor.executemany('INSERT INTO Owner (full_name, email, phone, password) VALUES (?, ?, ?, ?)', owners)

    # Providers matching exact quick demo buttons
    providers = [
        ("Dr. Sarah Jenkins", "Veterinarian", "9876543211", "sarah@petcare.in", "Happy Paws Clinic", 8, "BVSc", "1234"),
        ("Mike Ross", "Groomer", "9876543212", "mike@grooming.com", "Clean Paws Spa", 5, "Certified", "1234"),
        ("Alex Walker", "Pet Walker", "9876543213", "alex@walking.com", "Happy Tails Exercise", 4, "Pro Walker", "1234")
    ]
    cursor.executemany('INSERT INTO Service_Provider (full_name, role, phone, email, clinic_or_shop_name, experience_years, qualification, password) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', providers)

    services = [
        ('Comprehensive Health Checkup', 50.00, 'Detailed physical examination by a vet', 'Veterinary', 'https://images.unsplash.com/photo-1584132967334-10e028bd69f7?w=500'),
        ('Pet Vaccination & Immunization', 45.00, 'Essential shots and immunizations', 'Veterinary', 'https://images.unsplash.com/photo-1612531386530-97286d97c2d2?w=500'),
        ('Nutritional Diet Consultation', 40.00, 'Customized meal plan and diet advice', 'Veterinary', 'https://images.unsplash.com/photo-1535930891776-0c2dfb7fda1a?w=500'),
        ('Therapeutic Bath & Blow-dry', 35.00, 'Relaxing bath and blow-dry styling', 'Grooming', 'https://images.unsplash.com/photo-1516734212186-a967f81ad0d7?w=500'),
        ('Breed-Specific Haircut', 55.00, 'Professional styling and coat trimming', 'Grooming', 'https://images.unsplash.com/photo-1535930891776-0c2dfb7fda1a?w=500'),
        ('Professional Nail Cutting & Filing', 20.00, 'Safe and careful nail clipping', 'Grooming', 'https://images.unsplash.com/photo-1583337130417-3346a1be7dee?w=500'),
        ('Puppy Socialization & Exercise', 30.00, 'Early behavioral socialization walk', 'Walking', 'https://images.unsplash.com/photo-1601758228041-f3b2795255f1?w=500'),
        ('Agility Training Session', 50.00, 'Obstacle course and physical agility training', 'Walking', 'https://images.unsplash.com/photo-1548199973-03cce0bbc87b?w=500'),
        ('Structured Group Play Date', 25.00, 'Supervised group pet play session', 'Walking', 'https://images.unsplash.com/photo-1537151625747-768eb6cf92b2?w=500')
    ]
    cursor.executemany('INSERT INTO Service_Catalog (service_name, base_price, description, category, image_url) VALUES (?, ?, ?, ?, ?)', services)

    pets = [
        (1, "Rocky", "Dog", "Golden Retriever", 3, "Male"),
        (1, "Max", "Dog", "Beagle", 2, "Male"),
        (2, "Bella", "Cat", "Siamese", 2, "Female"),
        (2, "Luna", "Cat", "Persian", 3, "Female"),
        (3, "Bruno", "Dog", "Labrador", 4, "Male"),
        (3, "Daisy", "Dog", "Poodle", 2, "Female"),
        (4, "Zoe", "Cat", "British Shorthair", 3, "Female"),
        (4, "Charlie", "Dog", "Bulldog", 4, "Male"),
        (5, "Tyson", "Dog", "Rottweiler", 5, "Male"),
        (5, "Lola", "Cat", "Ragdoll", 1, "Female"),
        (6, "Cooper", "Dog", "Husky", 2, "Male"),
        (6, "Lucy", "Cat", "Sphynx", 2, "Female"),
        (7, "Milo", "Cat", "Bengal", 3, "Male"),
        (7, "Sadie", "Dog", "Boxer", 3, "Female"),
        (8, "Oliver", "Cat", "Abyssinian", 1, "Male"),
        (8, "Lily", "Dog", "Chihuahua", 2, "Female"),
        (9, "Simba", "Cat", "Maine Coon", 4, "Male"),
        (9, "Kiki", "Cat", "Domestic Shorthair", 2, "Female"),
        (10, "Buddy", "Dog", "German Shepherd", 3, "Male"),
        (10, "Coco", "Dog", "Shih Tzu", 2, "Female")
    ]
    cursor.executemany('INSERT INTO Pet (owner_id, name, species, breed, age, gender) VALUES (?, ?, ?, ?, ?, ?)', pets)

    bookings = [
        (1, 1, 1, 1, '2026-09-10', '10:00 AM', 'Confirmed'),
        (1, 2, 2, 1, '2026-09-11', '11:30 AM', 'Confirmed'),
        (2, 3, 4, 2, '2026-09-12', '08:00 AM', 'Confirmed'),
        (2, 4, 5, 2, '2026-09-13', '02:00 PM', 'Confirmed'),
        (3, 5, 7, 3, '2026-09-14', '09:00 AM', 'Pending'),
        (3, 6, 8, 3, '2026-09-15', '04:00 PM', 'Confirmed'),
        (4, 7, 1, 1, '2026-09-16', '10:30 AM', 'Confirmed'),
        (4, 8, 3, 1, '2026-09-17', '01:00 PM', 'Completed'),
        (5, 9, 6, 2, '2026-09-18', '07:30 AM', 'Confirmed'),
        (5, 10, 4, 2, '2026-09-19', '11:00 AM', 'Confirmed'),
        (6, 11, 7, 3, '2026-09-20', '03:30 PM', 'Pending'),
        (6, 12, 9, 3, '2026-09-21', '08:30 AM', 'Confirmed'),
        (7, 13, 2, 1, '2026-09-22', '09:30 AM', 'Confirmed'),
        (8, 15, 5, 2, '2026-09-23', '10:00 AM', 'Completed'),
        (9, 17, 8, 3, '2026-09-24', '05:00 PM', 'Confirmed')
    ]
    cursor.executemany('INSERT INTO Booking (owner_id, pet_id, service_id, provider_id, booking_date, booking_time, status) VALUES (?, ?, ?, ?, ?, ?, ?)', bookings)

    conn.commit()
    conn.close()
    print("Database rebuilt with exact demo credentials!")

if __name__ == '__main__':
    rebuild_database()

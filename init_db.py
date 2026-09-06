import sqlite3
import os

def init_db():
    if os.path.exists('petcare.db'):
        os.remove('petcare.db')
        
    conn = sqlite3.connect('petcare.db')
    cursor = conn.cursor()

    # Create Tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Owner (
            owner_id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Pet (
            pet_id INTEGER PRIMARY KEY AUTOINCREMENT,
            owner_id INTEGER,
            name TEXT NOT NULL,
            species TEXT NOT NULL,
            breed TEXT NOT NULL,
            age INTEGER CHECK(age > 0),
            gender TEXT,
            FOREIGN KEY (owner_id) REFERENCES Owner(owner_id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Service_Provider (
            provider_id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT NOT NULL,
            role TEXT NOT NULL,
            clinic_or_shop_name TEXT,
            experience_years INTEGER,
            qualification TEXT,
            password TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Service_Catalog (
            service_id INTEGER PRIMARY KEY AUTOINCREMENT,
            service_name TEXT NOT NULL,
            category TEXT NOT NULL,
            base_price REAL NOT NULL,
            description TEXT,
            image_url TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Booking (
            booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
            owner_id INTEGER,
            pet_id INTEGER,
            service_id INTEGER,
            provider_id INTEGER,
            booking_date TEXT,
            booking_time TEXT,
            status TEXT DEFAULT 'Confirmed',
            FOREIGN KEY (owner_id) REFERENCES Owner(owner_id),
            FOREIGN KEY (pet_id) REFERENCES Pet(pet_id),
            FOREIGN KEY (service_id) REFERENCES Service_Catalog(service_id),
            FOREIGN KEY (provider_id) REFERENCES Service_Provider(provider_id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Medical_Record (
            record_id INTEGER PRIMARY KEY AUTOINCREMENT,
            pet_id INTEGER,
            provider_id INTEGER,
            author_name TEXT,
            diagnosis TEXT,
            treatment TEXT,
            date_recorded TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (pet_id) REFERENCES Pet(pet_id),
            FOREIGN KEY (provider_id) REFERENCES Service_Provider(provider_id)
        )
    ''')

    # Seed 5 Pet Owners
    owners_data = [
        ("Alex Turner", "alex@test.com", "9876543210", "1234"),
        ("Priya Sharma", "priya@test.com", "9123456789", "1234"),
        ("David Miller", "david@test.com", "9811223344", "1234"),
        ("Ananya Roy", "ananya@test.com", "9722334455", "1234"),
        ("Carlos Gomez", "carlos@test.com", "9633445566", "1234")
    ]
    cursor.executemany("INSERT INTO Owner (full_name, email, phone, password) VALUES (?, ?, ?, ?)", owners_data)

    # Seed 15 Pets
    pets_data = [
        (1, "Rocky", "Dog", "German Shepherd", 4, "Male"),
        (1, "Max", "Dog", "Golden Retriever", 3, "Male"),
        (1, "Coco", "Dog", "Poodle", 2, "Female"),
        (2, "Bella", "Cat", "Siamese", 2, "Female"),
        (2, "Luna", "Cat", "Persian", 2, "Female"),
        (2, "Simba", "Cat", "Maine Coon", 3, "Male"),
        (3, "Bruno", "Dog", "Bulldog", 5, "Male"),
        (3, "Daisy", "Dog", "Beagle", 3, "Female"),
        (3, "Milo", "Cat", "British Shorthair", 1, "Male"),
        (4, "Zoe", "Bird", "Parakeet", 1, "Female"),
        (4, "Charlie", "Dog", "Labrador", 4, "Male"),
        (4, "Kiki", "Bird", "Cockatiel", 2, "Female"),
        (5, "Tyson", "Dog", "Boxer", 4, "Male"),
        (5, "Lola", "Cat", "Ragdoll", 2, "Female"),
        (5, "Oscar", "Dog", "Shih Tzu", 3, "Male")
    ]
    cursor.executemany("INSERT INTO Pet (owner_id, name, species, breed, age, gender) VALUES (?, ?, ?, ?, ?, ?)", pets_data)

    # Seed Service Providers
    providers_data = [
        ("Dr. Sarah Jenkins", "sarah@petcare.in", "9988776655", "Veterinarian", "Paws Clinic", 8, "BVSc & AH", "1234"),
        ("Emily Blunt", "emily@petcare.in", "9977665544", "Groomer", "Glamour Paws", 5, "Certified Stylist", "1234"),
        ("Mike Ross", "mike@petcare.in", "9966554433", "Walker", "Active Tails Walking", 4, "Professional Trainer", "1234")
    ]
    cursor.executemany("INSERT INTO Service_Provider (full_name, email, phone, role, clinic_or_shop_name, experience_years, qualification, password) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", providers_data)

    # Seed 12 Services Catalog
    services_data = [
        ("Pet Vaccination & Immunization", "Veterinary", 1200.0, "Essential core and non-core vaccinations to protect your pet against viral infections.", "https://images.unsplash.com/photo-1612349317150-e413f6a5b16d?auto=format&fit=crop&w=600&q=80"),
        ("Comprehensive Health Checkup", "Veterinary", 1500.0, "Full physical examination including cardiac, dental, and orthopedic assessment by expert vets.", "https://images.unsplash.com/photo-1584132967334-10e028bd69f7?auto=format&fit=crop&w=600&q=80"),
        ("Parasite & Tick Treatment", "Veterinary", 850.0, "Advanced flea, tick, and deworming treatments to ensure optimal skin health.", "https://images.unsplash.com/photo-1576201836106-db1758fd1c97?auto=format&fit=crop&w=600&q=80"),
        ("Therapeutic Bath & Blowdry", "Grooming", 900.0, "Relaxing medicated bath with organic shampoo, blow dry, and deep coat conditioning.", "https://images.unsplash.com/photo-1516734212186-a967f81ad0d7?auto=format&fit=crop&w=600&q=80"),
        ("Coat Styling & Hair Trimming", "Grooming", 1200.0, "Breed-specific haircuts, sanitary trimming, matting removal, and stylish fur sculpting.", "https://images.unsplash.com/photo-1535930891776-0c2dfb7fda1a?auto=format&fit=crop&w=600&q=80"),
        ("Nail Trimming & Paw Care", "Grooming", 400.0, "Safe nail clipping, filing, and soothing paw pad moisturizing balm application.", "https://images.unsplash.com/photo-1548199973-03cce0bbc87b?auto=format&fit=crop&w=600&q=80"),
        ("Dental Cleaning & Hygiene", "Grooming", 1100.0, "Plaque removal, teeth brushing, and breath-freshening oral treatment for dental health.", "https://images.unsplash.com/photo-1583511655857-d19b40a7a54e?auto=format&fit=crop&w=600&q=80"),
        ("Energetic Daily Dog Walking", "Walking", 600.0, "1-hour structured outdoor walk, leash training, and cardiovascular exercise.", "https://images.unsplash.com/photo-1601758228041-f3b2795255f1?auto=format&fit=crop&w=600&q=80"),
        ("Obedience & Agility Training", "Walking", 1500.0, "Professional behavioral coaching, impulse control, and agility exercises for active dogs.", "https://images.unsplash.com/photo-1541599540903-216a46ca1dc0?auto=format&fit=crop&w=600&q=80"),
        ("Puppy Socialization Playdate", "Walking", 800.0, "Supervised group play and socialization session for puppies to build friendly social skills.", "https://images.unsplash.com/photo-1587300003388-59208cc962cb?auto=format&fit=crop&w=600&q=80"),
        ("Pet Boarding & Daycare", "Wellness", 1200.0, "Safe, affectionate overnight boarding with 24/7 supervision and playtime.", "https://images.unsplash.com/photo-1543466835-00a7907e9de1?auto=format&fit=crop&w=600&q=80"),
        ("Nutritional Diet Consultation", "Wellness", 950.0, "Customized meal planning and dietary counselling for pets with specific nutritional needs.", "https://images.unsplash.com/photo-1583337130417-3346a1be7dee?auto=format&fit=crop&w=600&q=80")
    ]
    cursor.executemany("INSERT INTO Service_Catalog (service_name, category, base_price, description, image_url) VALUES (?, ?, ?, ?, ?)", services_data)

    # Seed Bookings
    bookings_data = [
        (1, 1, 1, 1, "2026-09-10", "10:00 AM", "Confirmed"),
        (1, 2, 2, 2, "2026-09-11", "11:30 AM", "Confirmed"),
        (1, 3, 3, 3, "2026-09-12", "09:00 AM", "Pending"),
        (2, 4, 1, 1, "2026-09-13", "02:00 PM", "Confirmed"),
        (2, 5, 2, 2, "2026-09-14", "10:30 AM", "Confirmed"),
        (2, 6, 4, 1, "2026-09-15", "04:00 PM", "Pending"),
        (3, 7, 3, 3, "2026-09-16", "08:00 AM", "Confirmed"),
        (3, 8, 1, 1, "2026-09-17", "11:00 AM", "Confirmed"),
        (3, 9, 2, 2, "2026-09-18", "01:30 PM", "Pending"),
        (4, 10, 4, 1, "2026-09-19", "09:30 AM", "Confirmed"),
        (4, 11, 3, 3, "2026-09-20", "05:00 PM", "Confirmed"),
        (4, 12, 1, 1, "2026-09-21", "12:00 PM", "Confirmed"),
        (5, 13, 2, 2, "2026-09-22", "10:00 AM", "Pending"),
        (5, 14, 4, 1, "2026-09-23", "02:30 PM", "Confirmed"),
        (5, 15, 3, 3, "2026-09-24", "03:30 PM", "Confirmed")
    ]
    cursor.executemany('''
        INSERT INTO Booking (owner_id, pet_id, service_id, provider_id, booking_date, booking_time, status)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', bookings_data)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Review (
            review_id INTEGER PRIMARY KEY AUTOINCREMENT,
            booking_id INTEGER,
            rating INTEGER CHECK(rating BETWEEN 1 AND 5),
            comment TEXT,
            date_submitted TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (booking_id) REFERENCES Booking(booking_id)
        )
    ''')

    # Seed Sample Reviews
    reviews_data = [
        (1, 5, "Amazing service! Rocky loved it."),
        (2, 4, "Very professional grooming and gentle care.")
    ]
    cursor.executemany("INSERT INTO Review (booking_id, rating, comment) VALUES (?, ?, ?)", reviews_data)

    # Seed Medical Records for all 15 pets
    medical_records_data = [
        (1, 1, "Dr. Sarah Jenkins", "Annual Checkup", "Administered core vaccines. Health is optimal."),
        (2, 2, "Emily Blunt", "Coat Matting", "Performed gentle de-matting and therapeutic bath."),
        (3, 3, "Mike Ross", "Low Activity", "Recommended increasing daily walk duration to 60 minutes."),
        (4, 1, "Dr. Sarah Jenkins", "Minor Ear Infection", "Prescribed ear drops and cleaner for 7 days."),
        (5, 2, "Emily Blunt", "Flea Treatment", "Applied advanced topical parasite protection."),
        (6, 1, "Dr. Sarah Jenkins", "Dental Check", "Mild plaque buildup, scheduled cleaning."),
        (7, 3, "Mike Ross", "Joint Stiffness", "Recommended joint supplements and light exercise."),
        (8, 1, "Dr. Sarah Jenkins", "Vaccination Booster", "Given rabies and DHPP boosters successfully."),
        (9, 2, "Emily Blunt", "Nail Overgrowth", "Nails clipped and paw pads moisturized."),
        (10, 1, "Dr. Sarah Jenkins", "Respiratory Check", "Clear lungs, normal breathing rate."),
        (11, 3, "Mike Ross", "Leash Training", "Showed great improvement in pulling behavior."),
        (12, 1, "Dr. Sarah Jenkins", "Routine Deworming", "Oral dewormer administered."),
        (13, 2, "Emily Blunt", "Skin Conditioning", "Used hypoallergenic oatmeal shampoo for dry skin."),
        (14, 1, "Dr. Sarah Jenkins", "Cardiac Screening", "Normal heart rhythm and pulse rate."),
        (15, 3, "Mike Ross", "Agility Assessment", "Passed basic obedience and agility drills.")
    ]
    cursor.executemany('''
        INSERT INTO Medical_Record (pet_id, provider_id, author_name, diagnosis, treatment)
        VALUES (?, ?, ?, ?, ?)
    ''', medical_records_data)

    conn.commit()
    conn.close()
    print("Database re-initialized successfully with Medical_Record table and all records!")

if __name__ == '__main__':
    init_db()

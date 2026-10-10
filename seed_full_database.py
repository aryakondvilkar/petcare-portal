import sqlite3
import os

basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'petcare.db')

def seed_database():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 1. Create Tables if they don't exist
    cursor.executescript('''
        CREATE TABLE IF NOT EXISTS Owner (
            owner_id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT,
            password TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS Service_Provider (
            provider_id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            role TEXT NOT NULL,
            phone TEXT,
            email TEXT UNIQUE NOT NULL,
            clinic_or_shop_name TEXT,
            experience_years INTEGER,
            qualification TEXT,
            password TEXT DEFAULT 'password'
        );

        CREATE TABLE IF NOT EXISTS Service_Catalog (
            service_id INTEGER PRIMARY KEY AUTOINCREMENT,
            service_name TEXT NOT NULL,
            base_price DECIMAL,
            description TEXT
        );

        CREATE TABLE IF NOT EXISTS Pet (
            pet_id INTEGER PRIMARY KEY AUTOINCREMENT,
            owner_id INTEGER,
            name TEXT NOT NULL,
            species TEXT,
            breed TEXT,
            age INTEGER,
            gender TEXT,
            FOREIGN KEY (owner_id) REFERENCES Owner(owner_id)
        );

        CREATE TABLE IF NOT EXISTS Booking (
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

        CREATE TABLE IF NOT EXISTS Medical_Record (
            record_id INTEGER PRIMARY KEY AUTOINCREMENT,
            pet_id INTEGER,
            provider_id INTEGER,
            author_name TEXT,
            diagnosis TEXT,
            treatment TEXT,
            FOREIGN KEY (pet_id) REFERENCES Pet(pet_id),
            FOREIGN KEY (provider_id) REFERENCES Service_Provider(provider_id)
        );
    ''')

    # 2. Insert 10 Pet Owners
    owners = [
        ("Sarah Jenkins", "sarah@example.com", "555-0101", "password123"),
        ("Michael Chang", "michael@example.com", "555-0102", "password123"),
        ("Emily Blunt", "emily@example.com", "555-0103", "password123"),
        ("David Miller", "david@example.com", "555-0104", "password123"),
        ("Jessica Alba", "jessica@example.com", "555-0105", "password123"),
        ("Robert Downey", "robert@example.com", "555-0106", "password123"),
        ("Emma Watson", "emma@example.com", "555-0107", "password123"),
        ("Chris Evans", "chris@example.com", "555-0108", "password123"),
        ("Natalie Portman", "natalie@example.com", "555-0109", "password123"),
        ("Tom Holland", "tom@example.com", "555-0110", "password123")
    ]
    cursor.executemany('''
        INSERT OR IGNORE INTO Owner (full_name, email, phone, password)
        VALUES (?, ?, ?, ?)
    ''', owners)

    # 3. Insert Service Providers (Veterinarian, Groomer, Pet Walker)
    providers = [
        ("Dr. Aditi Sharma", "Veterinarian", "9876543210", "aditi@petclinic.com", "Happy Paws Clinic", 7, "BVSc & AH", "password123"),
        ("Jessica Taylor", "Groomer", "9876543212", "jessica@grooming.com", "Clean Paws Spa", 5, "Certified Groomer", "password123"),
        ("Alex Mercer", "Pet Walker", "9876543213", "alex@walking.com", "Happy Tails Exercise", 4, "Pro Pet Walker", "password123")
    ]
    cursor.executemany('''
        INSERT OR IGNORE INTO Service_Provider (full_name, role, phone, email, clinic_or_shop_name, experience_years, qualification, password)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', providers)

    # 4. Insert Service Catalog
    services = [
        ("Health Check & Vaccination", 50.00, "Comprehensive physical exam and standard vaccinations."),
        ("Bath & Blow-dry", 40.00, "Refreshing bath, shampoo, conditioning, and blow-dry styling."),
        ("Daily Pet Walking", 25.00, "1-hour energetic outdoor neighborhood walk and exercise.")
    ]
    cursor.executemany('''
        INSERT OR IGNORE INTO Service_Catalog (service_name, base_price, description)
        VALUES (?, ?, ?)
    ''', services)

    # 5. Insert 20 Pets (2 for each of the 10 owners)
    pets = [
        (1, "Max", "Dog", "Golden Retriever", 3, "Male"),
        (1, "Bella", "Cat", "Siamese", 2, "Female"),
        (2, "Charlie", "Dog", "Beagle", 4, "Male"),
        (2, "Luna", "Cat", "Persian", 3, "Female"),
        (3, "Cooper", "Dog", "Labrador", 5, "Male"),
        (3, "Lucy", "Cat", "Maine Coon", 2, "Female"),
        (4, "Rocky", "Dog", "German Shepherd", 4, "Male"),
        (4, "Daisy", "Dog", "Poodle", 2, "Female"),
        (5, "Milo", "Cat", "British Shorthair", 3, "Male"),
        (5, "Sadie", "Dog", "Boxer", 3, "Female"),
        (6, "Oliver", "Cat", "Ragdoll", 1, "Male"),
        (6, "Lola", "Dog", "Bulldog", 4, "Female"),
        (7, "Bailey", "Dog", "Siberian Husky", 2, "Male"),
        (7, "Zoe", "Cat", "Sphynx", 3, "Female"),
        (8, "Buddy", "Dog", "Rottweiler", 4, "Male"),
        (8, "Molly", "Dog", "Cocker Spaniel", 5, "Female"),
        (9, "Teddy", "Dog", "Shih Tzu", 2, "Male"),
        (9, "Chloe", "Cat", "Abyssinian", 1, "Female"),
        (10, "Leo", "Cat", "Bengal", 2, "Male"),
        (10, "Lily", "Dog", "Chihuahua", 3, "Female")
    ]
    cursor.executemany('''
        INSERT OR IGNORE INTO Pet (owner_id, name, species, breed, age, gender)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', pets)

    # 6. Insert 15+ Booked Appointments mapped properly to providers & services
    # Provider 1 = Vet (ID 1), Provider 2 = Groomer (ID 2), Provider 3 = Walker (ID 3)
    # Service 1 = Health Check (ID 1), Service 2 = Bath & Blow-dry (ID 2), Service 3 = Daily Walking (ID 3)
   # 6. Insert 15+ Unique Booked Appointments mapped properly across 10 owners & 20 pets
    bookings = [
        (1, 1, 1, 1, '2026-06-10', '10:00 AM', 'Confirmed'),  # Owner 1, Pet 1 -> Vet
        (1, 2, 2, 2, '2026-06-11', '11:30 AM', 'Completed'),  # Owner 1, Pet 2 -> Groomer
        (2, 3, 3, 3, '2026-06-12', '08:00 AM', 'Confirmed'),  # Owner 2, Pet 3 -> Walker
        (2, 4, 1, 1, '2026-06-13', '02:00 PM', 'Confirmed'),  # Owner 2, Pet 4 -> Vet
        (3, 5, 2, 2, '2026-06-14', '09:00 AM', 'Pending'),    # Owner 3, Pet 5 -> Groomer
        (3, 6, 3, 3, '2026-06-15', '04:00 PM', 'Confirmed'),  # Owner 3, Pet 6 -> Walker
        (4, 7, 1, 1, '2026-06-16', '10:30 AM', 'Confirmed'),  # Owner 4, Pet 7 -> Vet
        (4, 8, 2, 2, '2026-06-17', '01:00 PM', 'Completed'),  # Owner 4, Pet 8 -> Groomer
        (5, 9, 3, 3, '2026-06-18', '07:30 AM', 'Confirmed'),  # Owner 5, Pet 9 -> Walker
        (5, 10, 1, 1, '2026-06-19', '11:00 AM', 'Confirmed'), # Owner 5, Pet 10 -> Vet
        (6, 11, 2, 2, '2026-06-20', '03:30 PM', 'Pending'),   # Owner 6, Pet 11 -> Groomer
        (6, 12, 3, 3, '2026-06-21', '08:30 AM', 'Confirmed'), # Owner 6, Pet 12 -> Walker
        (7, 13, 1, 1, '2026-06-22', '09:30 AM', 'Confirmed'), # Owner 7, Pet 13 -> Vet
        (8, 15, 2, 2, '2026-06-23', '10:00 AM', 'Completed'), # Owner 8, Pet 15 -> Groomer
        (9, 17, 3, 3, '2026-06-24', '05:00 PM', 'Confirmed')  # Owner 9, Pet 17 -> Walker
    ]
    cursor.executemany('''
        INSERT OR IGNORE INTO Booking (owner_id, pet_id, service_id, provider_id, booking_date, booking_time, status)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', bookings)

    conn.commit()
    conn.close()
    print("Database successfully seeded with 10 owners, 20 pets, providers, catalog, and 15 appointments!")

if __name__ == '__main__':
    seed_database()
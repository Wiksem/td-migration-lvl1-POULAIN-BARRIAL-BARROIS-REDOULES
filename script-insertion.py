from faker import Faker
import mysql.connector
import random
from datetime import date

fake = Faker("fr_FR")

# Connexion MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",      
    database="ReservationVoyage"
)

cursor = conn.cursor()

# -----------------------
# Insertion -  500 utilisateurs
# -----------------------
users_ids = []

for _ in range(500):
    nom = fake.last_name()
    prenom = fake.first_name()
    email = fake.unique.email()
    motdepasse = fake.password(length=12)

    cursor.execute(
        """
        INSERT INTO Utilisateurs (Nom, Prenom, Email, MotDePasse)
        VALUES (%s, %s, %s, %s)
        """,
        (nom, prenom, email, motdepasse)
    )
    users_ids.append(cursor.lastrowid)

conn.commit()

# -----------------------
# Insertion - 1000 réservations
# -----------------------
destinations = [
    "Paris", "Londres", "New York", "Tokyo",
    "Rome", "Berlin", "Madrid", "Lisbonne"
]

for _ in range(1000):
    utilisateur_id = random.choice(users_ids)
    destination = random.choice(destinations)
    date_reservation = fake.date_between(start_date="-1y", end_date="today")
    prix = round(random.uniform(80, 1500), 2)

    cursor.execute(
        """
        INSERT INTO Reservations (UtilisateurId, Destination, DateReservation, Prix)
        VALUES (%s, %s, %s, %s)
        """,
        (utilisateur_id, destination, date_reservation, prix)
    )

conn.commit()

cursor.close()
conn.close()

print("Utilisateurs et réservations insérés.")

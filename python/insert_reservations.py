import mysql.connector
from faker import Faker
import random
from datetime import datetime, timedelta


conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",  
    database="ReservationVoyage"
)

cursor = conn.cursor()
fake = Faker("fr_FR")


cursor.execute("SELECT Id FROM Utilisateurs")
user_ids = [row[0] for row in cursor.fetchall()]

destinations = [
    "Paris", "Londres", "New York", "Tokyo", "Rome",
    "Barcelone", "Berlin", "Lisbonne", "Dubaï", "Montréal"
]

def random_date():

    today = datetime.today()
    delta = timedelta(days=random.randint(1, 365))
    return (today + delta).date()

nb_reservations = 1000

for _ in range(nb_reservations):
    utilisateur_id = random.choice(user_ids)
    destination = random.choice(destinations)
    date_depart = random_date()
    prix = round(random.uniform(50, 1500), 2)

    cursor.execute(
        """
        INSERT INTO Reservations (UtilisateurId, Destination, DateDepart, Prix)
        VALUES (%s, %s, %s, %s)
        """,
        (utilisateur_id, destination, date_depart, prix)
    )

conn.commit()
cursor.close()
conn.close()
print(f"{nb_reservations} réservations insérées avec succès.")

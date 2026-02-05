import time
import random
from datetime import datetime, timedelta

from faker import Faker
import mysql.connector

fake = Faker("fr_FR")

# Attendre que MySQL soit prêt (retry avec backoff)
print("Attente de MySQL...")
max_retries = 30
retry_count = 0
conn = None

while retry_count < max_retries:
    try:
        conn = mysql.connector.connect(
            host="gt_mysql",
            user="gt_user",
            password="gt_pass",
            database="globetrotter"
        )
        print("Connexion MySQL établie!")
        break
    except mysql.connector.Error as e:
        retry_count += 1
        print(f"Tentative {retry_count}/{max_retries} : {e}")
        time.sleep(2)

if conn is None:
    print("Impossible de se connecter à MySQL après plusieurs tentatives.")
    exit(1)

cur = conn.cursor(dictionary=True)

def random_dates():
    """Génère une paire (departure_date, return_date)."""
    start = datetime.today() + timedelta(days=random.randint(1, 180))
    end = start + timedelta(days=random.randint(3, 21))
    return start.date(), end.date()


def insert_booking():
    dep, ret = random_dates()
    cur.execute(
        """
        INSERT INTO bookings (customer_email, destination, departure_date, return_date, status)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (
            fake.unique.email(),
            random.choice(["Paris", "Tokyo", "New York", "Rome", "Berlin", "Madrid", "Londres"]),
            dep,
            ret,
            random.choice(["pending", "confirmed", "cancelled"])
        )
    )
    conn.commit()


def update_random_booking():
    """Met à jour aléatoirement le status ou la return_date d'une réservation existante."""
    cur.execute("SELECT id FROM bookings ORDER BY RAND() LIMIT 1")
    row = cur.fetchone()
    if not row:
        return  # aucune réservation à mettre à jour

    booking_id = row["id"]

    if random.choice([True, False]):
        # changer le status
        new_status = random.choice(["pending", "confirmed", "cancelled"])
        cur.execute(
            "UPDATE bookings SET status = %s WHERE id = %s",
            (new_status, booking_id)
        )
    else:
        # changer la date de retour
        _, new_return = random_dates()
        cur.execute(
            "UPDATE bookings SET return_date = %s WHERE id = %s",
            (new_return, booking_id)
        )

    conn.commit()


print("Démarrage du générateur de trafic (Faker) sur MySQL...")
try:
    while True:
        insert_booking()
        update_random_booking()
        # pause de 2 secondes pour simuler un trafic régulier
        time.sleep(2)
except KeyboardInterrupt:
    print("Arrêt du générateur de trafic.")
finally:
    cur.close()
    conn.close()

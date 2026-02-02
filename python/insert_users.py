import mysql.connector
from faker import Faker
import random
import string


conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="ReservationVoyage"
)

cursor = conn.cursor()
fake = Faker("fr_FR")

def random_password(length=12):
    chars = string.ascii_letters + string.digits
    return "".join(random.choice(chars) for _ in range(length))

nb_users = 500

for _ in range(nb_users):
    nom = fake.last_name()
    prenom = fake.first_name()
    email = fake.unique.email()
    mot_de_passe = random_password()

    cursor.execute(
        """
        INSERT INTO Utilisateurs (Nom, Prenom, Email, MotDePasse)
        VALUES (%s, %s, %s, %s)
        """,
        (nom, prenom, email, mot_de_passe)
    )

conn.commit()
cursor.close()
conn.close()
print(f"{nb_users} utilisateurs insérés avec succès.")

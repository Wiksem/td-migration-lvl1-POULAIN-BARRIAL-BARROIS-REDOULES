import mysql.connector
import psycopg2

# Connexion MySQL
mysql_conn = mysql.connector.connect(
    host="localhost",
    port=3307,
    user="gt_user",
    password="gt_pass",
    database="globetrotter"
)
mysql_cur = mysql_conn.cursor(dictionary=True)

# Connexion PostgreSQL
pg_conn = psycopg2.connect(
    host="localhost",
    port=5433,
    user="gt_user",
    password="gt_pass",
    database="globetrotter"
)
pg_cur = pg_conn.cursor()

# La table existe déjà (créée par Flyway), on la vide au cas où
print("Nettoyage de la table PostgreSQL...")
pg_cur.execute("TRUNCATE TABLE bookings;")
pg_conn.commit()

# Copier toutes les données
print("Copie des données depuis MySQL...")
mysql_cur.execute("SELECT * FROM bookings")
rows = mysql_cur.fetchall()

print(f"Trouvé {len(rows)} lignes dans MySQL. Insertion dans PostgreSQL...")

for row in rows:
    pg_cur.execute(
        """
        INSERT INTO bookings (id, customer_email, destination, departure_date, return_date, status, updated_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """,
        (row['id'], row['customer_email'], row['destination'], row['departure_date'], 
         row['return_date'], row['status'], row['updated_at'])
    )

pg_conn.commit()
print(f"✓ Migration initiale terminée : {len(rows)} bookings copiées dans PostgreSQL.")

mysql_cur.close()
mysql_conn.close()
pg_cur.close()
pg_conn.close()

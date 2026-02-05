import mysql.connector
import psycopg2

# Connexion MySQL (depuis l'hôte vers le conteneur)
mysql_conn = mysql.connector.connect(
    host="localhost",
    port=3307,
    user="gt_user",
    password="gt_pass",
    database="globetrotter"
)
mysql_cur = mysql_conn.cursor(dictionary=True)

# Connexion PostgreSQL (depuis l'hôte vers le conteneur)
pg_conn = psycopg2.connect(
    host="localhost",
    port=5433,
    user="gt_user",
    password="gt_pass",
    database="globetrotter"
)
pg_cur = pg_conn.cursor()

# Créer la table dans PostgreSQL
print("Création de la table bookings dans PostgreSQL...")
pg_cur.execute("""
    DROP TABLE IF EXISTS bookings;
    CREATE TABLE bookings (
        id BIGINT PRIMARY KEY,
        customer_email VARCHAR(255) NOT NULL,
        destination VARCHAR(255) NOT NULL,
        departure_date DATE NOT NULL,
        return_date DATE NOT NULL,
        status VARCHAR(50) NOT NULL,
        updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
    );
""")
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

-- Version PostgreSQL adaptée depuis MySQL dump

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

-- Insertion des 242 lignes (copie directement depuis ton dump)
INSERT INTO bookings VALUES (1,'xgarnier@example.net','Berlin','2026-06-19','2026-05-24','cancelled','2026-02-05 10:54:36'),(2,'claude39@example.org','Madrid','2026-06-23','2026-05-30','pending','2026-02-05 10:55:08'),
-- ... [colle toutes les lignes INSERT de ton dump original, en enlevant les backticks]
-- jusqu'à la ligne 242
(242,'jacqueline00@example.com','Madrid','2026-04-03','2026-04-24','pending','2026-02-05 11:00:09');

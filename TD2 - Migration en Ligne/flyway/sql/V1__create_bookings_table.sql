-- Migration V1 : Création de la table bookings dans PostgreSQL

CREATE TABLE IF NOT EXISTS bookings (
    id BIGINT PRIMARY KEY,
    customer_email VARCHAR(255) NOT NULL,
    destination VARCHAR(255) NOT NULL,
    departure_date DATE NOT NULL,
    return_date DATE NOT NULL,
    status VARCHAR(50) NOT NULL,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Index sur updated_at pour optimiser le CDC
CREATE INDEX IF NOT EXISTS idx_bookings_updated_at ON bookings(updated_at);

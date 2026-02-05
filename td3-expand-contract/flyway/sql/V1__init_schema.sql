
CREATE TABLE bookings (
    id BIGSERIAL PRIMARY KEY,
    customer_first_name VARCHAR(100) NOT NULL,
    customer_last_name VARCHAR(100) NOT NULL,
    customer_email VARCHAR(255) NOT NULL,
    destination VARCHAR(255) NOT NULL,
    departure_date DATE NOT NULL,
    return_date DATE NOT NULL,
    status VARCHAR(50) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Insertion de quelques données de test
INSERT INTO bookings (customer_first_name, customer_last_name, customer_email, destination, departure_date, return_date, status) VALUES
('Jean', 'Dupont', 'jean.dupont@example.com', 'Paris', '2026-03-15', '2026-03-20', 'PENDING'),
('Marie', 'Martin', 'marie.martin@example.com', 'Londres', '2026-04-10', '2026-04-15', 'CONFIRMED'),
('Pierre', 'Durand', 'pierre.durand@example.com', 'Rome', '2026-05-01', '2026-05-07', 'CONFIRMED'),
('Sophie', 'Bernard', 'sophie.bernard@example.com', 'Madrid', '2026-06-12', '2026-06-18', 'CANCELLED'),
('Luc', 'Petit', 'luc.petit@example.com', 'Berlin', '2026-07-20', '2026-07-25', 'PENDING');

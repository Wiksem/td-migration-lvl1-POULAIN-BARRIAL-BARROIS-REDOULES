-- V2__expand_bookings.sql
-- Phase EXPAND : ajout des nouvelles colonnes sans casser l'ancien schéma

-- 1. Ajouter la nouvelle colonne customer_full_name (nullable pour l'instant)
ALTER TABLE bookings
ADD COLUMN customer_full_name VARCHAR(200);

-- 2. Ajouter la colonne last_modified_at
ALTER TABLE bookings
ADD COLUMN last_modified_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP;

-- 3. Créer la table de référence des statuts
CREATE TABLE booking_status_ref (
    code VARCHAR(50) PRIMARY KEY,
    label VARCHAR(255) NOT NULL
);

-- 4. Insérer les statuts de référence
INSERT INTO booking_status_ref (code, label) VALUES
('PENDING', 'En attente de paiement'),
('CONFIRMED', 'Réservation confirmée'),
('CANCELLED', 'Réservation annulée');

-- Note : La colonne 'status' reste pour l'instant (compatibilité avec ancienne appli V1)
-- À terme, elle pointera vers booking_status_ref.code

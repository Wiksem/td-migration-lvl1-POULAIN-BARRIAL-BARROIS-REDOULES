-- V4__contract_drop_old_columns.sql
-- Phase CONTRACT : nettoyage de l'ancien schéma (après déploiement nouvelle appli V2)

-- 1. Rendre customer_full_name obligatoire (NOT NULL)
ALTER TABLE bookings
ALTER COLUMN customer_full_name SET NOT NULL;

-- 2. Supprimer les anciennes colonnes first_name et last_name
ALTER TABLE bookings
DROP COLUMN customer_first_name,
DROP COLUMN customer_last_name;

-- 3. (Optionnel) Remplacer la colonne 'status' par une foreign key vers booking_status_ref
-- Pour simplifier, on va juste ajouter une contrainte CHECK

ALTER TABLE bookings
ADD CONSTRAINT check_status_valid
CHECK (status IN (SELECT code FROM booking_status_ref));

-- Ajouter un commentaire pour documenter la relation
COMMENT ON COLUMN bookings.status IS 'Référence vers booking_status_ref.code';

-- Note : Après V4, l'ancienne version de l'application (V1) ne fonctionnera plus
-- car les colonnes customer_first_name et customer_last_name n'existent plus

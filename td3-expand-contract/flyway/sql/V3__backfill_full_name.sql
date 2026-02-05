-- V3__backfill_full_name.sql
-- Phase TRANSITION : migration des données existantes

-- 1. Remplir customer_full_name pour toutes les lignes existantes
UPDATE bookings
SET customer_full_name = customer_first_name || ' ' || customer_last_name
WHERE customer_full_name IS NULL;

-- 2. Créer un trigger pour maintenir customer_full_name automatiquement
-- Ce trigger maintient la cohérence tant que les anciennes colonnes existent

CREATE OR REPLACE FUNCTION sync_customer_full_name()
RETURNS TRIGGER AS $$
BEGIN
    -- Si les colonnes first_name et last_name existent et sont remplies
    IF NEW.customer_first_name IS NOT NULL AND NEW.customer_last_name IS NOT NULL THEN
        NEW.customer_full_name := NEW.customer_first_name || ' ' || NEW.customer_last_name;
    END IF;
    
    -- Mettre à jour last_modified_at
    NEW.last_modified_at := CURRENT_TIMESTAMP;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_sync_customer_full_name
BEFORE INSERT OR UPDATE ON bookings
FOR EACH ROW
EXECUTE FUNCTION sync_customer_full_name();

-- 3. Vérifier que les statuts correspondent aux codes de référence
-- (Optionnel : normaliser les statuts si besoin)
UPDATE bookings
SET status = 'PENDING'
WHERE status NOT IN (SELECT code FROM booking_status_ref);

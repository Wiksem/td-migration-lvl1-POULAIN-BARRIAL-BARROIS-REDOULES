USE ReservationVoyage;

DELIMITER $$

CREATE PROCEDURE GenerateReservations(IN num_reservations INT)
BEGIN
    DECLARE i INT DEFAULT 0;
    DECLARE user_id INT;
    DECLARE destination VARCHAR(255);
    DECLARE date_depart DATE;
    DECLARE date_retour DATE;
    DECLARE prix DECIMAL(10,2);
    DECLARE statut VARCHAR(20);
    DECLARE destinations_count INT DEFAULT 8;
    
    WHILE i < num_reservations DO
        -- Sélectionner un utilisateur aléatoire (entre 1 et 500)
        SET user_id = FLOOR(1 + RAND() * 500);
        
        -- Sélectionner une destination aléatoire
        SET destination = ELT(FLOOR(1 + RAND() * destinations_count), 
            'Paris', 'Londres', 'Rome', 'Madrid', 
            'Berlin', 'Lisbonne', 'Amsterdam', 'Barcelone');
        
        -- Générer une date de départ (entre aujourd'hui et +365 jours)
        SET date_depart = DATE_ADD(CURDATE(), INTERVAL FLOOR(RAND() * 365) DAY);
        
        -- Générer une date de retour (3 à 21 jours après le départ)
        SET date_retour = DATE_ADD(date_depart, INTERVAL FLOOR(3 + RAND() * 18) DAY);
        
        -- Générer un prix aléatoire (entre 150 et 2500 euros)
        SET prix = ROUND(150 + RAND() * 2350, 2);
        
        -- Sélectionner un statut aléatoire
        SET statut = ELT(FLOOR(1 + RAND() * 3), 'en_attente', 'confirmee', 'annulee');
        
        -- Insérer la réservation
        INSERT INTO Reservations (UtilisateurId, Destination, DateDepart, DateRetour, Prix, Statut)
        VALUES (user_id, destination, date_depart, date_retour, prix, statut);
        
        SET i = i + 1;
    END WHILE;
END$$

DELIMITER ;

-- Exécuter la procédure pour générer 1000 réservations
CALL GenerateReservations(1000);

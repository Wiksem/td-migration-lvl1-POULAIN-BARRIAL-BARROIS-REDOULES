USE ReservationVoyage;

DELIMITER $$

CREATE PROCEDURE GenerateUsers(IN num_users INT)
BEGIN
    DECLARE i INT DEFAULT 0;
    DECLARE nom VARCHAR(100);
    DECLARE prenom VARCHAR(100);
    DECLARE email VARCHAR(255);
    DECLARE password_hash VARCHAR(255);
    
    WHILE i < num_users DO
        -- Générer des données aléatoires
        SET nom = CONCAT('Nom', FLOOR(1 + RAND() * 9999));
        SET prenom = CONCAT('Prenom', FLOOR(1 + RAND() * 9999));
        SET email = CONCAT('user', i, '@example.com');
        SET password_hash = MD5(CONCAT('password', RAND()));
        
        -- Insérer l'utilisateur
        INSERT INTO Utilisateurs (Nom, Prenom, Email, MotDePasse)
        VALUES (nom, prenom, email, password_hash);
        
        SET i = i + 1;
    END WHILE;
END$$

DELIMITER ;

-- Exécuter la procédure pour générer 500 utilisateurs
CALL GenerateUsers(500);

-- Création de la base de données
CREATE DATABASE IF NOT EXISTS ReservationVoyage 
DEFAULT CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

USE ReservationVoyage;

-- Table Utilisateurs
CREATE TABLE Utilisateurs (
    Id INT AUTO_INCREMENT PRIMARY KEY,
    Nom VARCHAR(100) NOT NULL,
    Prenom VARCHAR(100) NOT NULL,
    Email VARCHAR(255) NOT NULL UNIQUE,
    MotDePasse VARCHAR(255) NOT NULL,
    DateCreation TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table Reservations
CREATE TABLE Reservations (
    Id INT AUTO_INCREMENT PRIMARY KEY,
    UtilisateurId INT NOT NULL,
    Destination VARCHAR(255) NOT NULL,
    DateDepart DATE NOT NULL,
    DateRetour DATE NOT NULL,
    Prix DECIMAL(10,2) NOT NULL,
    Statut ENUM('en_attente', 'confirmee', 'annulee') DEFAULT 'en_attente',
    DateReservation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (UtilisateurId) REFERENCES Utilisateurs(Id) ON DELETE CASCADE
);
CREATE DATABASE ReservationVoyage
  DEFAULT CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE ReservationVoyage;

CREATE TABLE Utilisateurs (
  Id INT AUTO_INCREMENT PRIMARY KEY,
  Nom VARCHAR(100) NOT NULL,
  Prenom VARCHAR(100) NOT NULL,
  Email VARCHAR(255) NOT NULL,
  MotDePasse VARCHAR(255) NOT NULL
);

CREATE TABLE Reservations (
  Id INT AUTO_INCREMENT PRIMARY KEY,
  UtilisateurId INT NOT NULL,
  Destination VARCHAR(100) NOT NULL,
  DateDepart DATE NOT NULL,
  Prix DECIMAL(10,2) NOT NULL,
  CONSTRAINT fk_res_user FOREIGN KEY (UtilisateurId)
    REFERENCES Utilisateurs(Id)
);

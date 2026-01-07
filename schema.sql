-- CS2 E-SPORT MANAGEMENT SYSTEM - DATABASE SCHEMA
-- Autor: Joel - BTS Datenbankprojekt | Datum: Januar 2025 | DB: MariaDB/MySQL | 3NF

CREATE DATABASE IF NOT EXISTS cs2_esport_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE cs2_esport_db;

SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS MATCHES, TOURNAMENTS, PLAYERS, TEAMS, USERS;
SET FOREIGN_KEY_CHECKS = 1;

CREATE TABLE USERS (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('Admin', 'Manager', 'Viewer') NOT NULL DEFAULT 'Viewer',
    email VARCHAR(100) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE TEAMS (
    team_id INT AUTO_INCREMENT PRIMARY KEY,
    team_name VARCHAR(100) NOT NULL UNIQUE,
    abbreviation VARCHAR(10) UNIQUE,
    country VARCHAR(50),
    founded_date DATE,
    coach VARCHAR(100),
    is_active BOOLEAN DEFAULT TRUE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE PLAYERS (
    player_id INT AUTO_INCREMENT PRIMARY KEY,
    team_id INT,
    nickname VARCHAR(50) NOT NULL UNIQUE,
    real_name VARCHAR(100),
    nationality VARCHAR(50),
    role ENUM('IGL', 'AWPer', 'Entry Fragger', 'Support', 'Lurker'),
    birth_date DATE,
    is_active BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (team_id) REFERENCES TEAMS(team_id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE TOURNAMENTS (
    tournament_id INT AUTO_INCREMENT PRIMARY KEY,
    tournament_name VARCHAR(150) NOT NULL,
    location VARCHAR(100),
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    prize_pool DECIMAL(12, 2),
    tier ENUM('S-Tier', 'A-Tier', 'B-Tier', 'C-Tier') DEFAULT 'B-Tier',
    status ENUM('Upcoming', 'Ongoing', 'Completed', 'Cancelled') DEFAULT 'Upcoming'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE MATCHES (
    match_id INT AUTO_INCREMENT PRIMARY KEY,
    tournament_id INT NOT NULL,
    team1_id INT NOT NULL,
    team2_id INT NOT NULL,
    score_team1 INT DEFAULT 0,
    score_team2 INT DEFAULT 0,
    match_date DATETIME NOT NULL,
    best_of ENUM('BO1', 'BO3', 'BO5') DEFAULT 'BO3',
    stage VARCHAR(50),
    winner_team_id INT,
    FOREIGN KEY (tournament_id) REFERENCES TOURNAMENTS(tournament_id) ON DELETE CASCADE,
    FOREIGN KEY (team1_id) REFERENCES TEAMS(team_id),
    FOREIGN KEY (team2_id) REFERENCES TEAMS(team_id),
    FOREIGN KEY (winner_team_id) REFERENCES TEAMS(team_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- BEISPIELDATEN
INSERT INTO USERS (username, password_hash, role, email) VALUES
('admin', 'hashed_pw', 'Admin', 'admin@cs2esport.de'),
('manager', 'hashed_pw', 'Manager', 'manager@cs2esport.de');

INSERT INTO TEAMS (team_name, abbreviation, country, coach) VALUES
('Natus Vincere', 'NaVi', 'Ukraine', 'Gorodenskyi'),
('FaZe Clan', 'FaZe', 'USA', 'Kubski'),
('G2 Esports', 'G2', 'Germany', 'Quoniam'),
('Team Vitality', 'VIT', 'France', 'Music');

INSERT INTO PLAYERS (team_id, nickname, real_name, nationality, role, birth_date) VALUES
(1, 's1mple', 'Oleksandr Kostyliev', 'Ukraine', 'AWPer', '1997-10-02'),
(1, 'b1t', 'Valeriy Vakhovskyi', 'Ukraine', 'Entry Fragger', '2003-01-05'),
(2, 'karrigan', 'Finn Andersen', 'Denmark', 'IGL', '1990-04-14'),
(2, 'ropz', 'Robin Kool', 'Estonia', 'Lurker', '1999-12-22'),
(3, 'NiKo', 'Nikola Kovac', 'Bosnia', 'Entry Fragger', '1997-02-16'),
(3, 'm0NESY', 'Ilya Osipov', 'Russia', 'AWPer', '2005-05-01'),
(4, 'ZywOo', 'Mathieu Herbaut', 'France', 'AWPer', '2000-11-09');

INSERT INTO TOURNAMENTS (tournament_name, location, start_date, end_date, prize_pool, tier, status) VALUES
('BLAST Premier 2025', 'Abu Dhabi', '2025-01-22', '2025-01-26', 1000000, 'S-Tier', 'Upcoming'),
('IEM Katowice 2025', 'Poland', '2025-02-01', '2025-02-09', 1000000, 'S-Tier', 'Upcoming'),
('PGL Major 2024', 'Copenhagen', '2024-03-17', '2024-03-31', 1250000, 'S-Tier', 'Completed');

INSERT INTO MATCHES (tournament_id, team1_id, team2_id, score_team1, score_team2, match_date, best_of, stage, winner_team_id) VALUES
(3, 1, 2, 2, 1, '2024-03-31 18:00:00', 'BO5', 'Grand Final', 1),
(3, 1, 3, 2, 0, '2024-03-30 15:00:00', 'BO3', 'Semi-Final', 1);

SELECT 'Schema erstellt!' AS Status;

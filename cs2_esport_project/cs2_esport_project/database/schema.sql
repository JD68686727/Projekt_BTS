-- ============================================================================
-- CS2 E-SPORT MANAGEMENT SYSTEM - DATABASE SCHEMA
-- ============================================================================
-- Projekt:     CS2 E-Sport Organisation Management
-- Autor:       Joel - BTS Datenbankprojekt
-- Datum:       Januar 2025
-- Datenbank:   MariaDB 10.x / MySQL 8.0+
-- Normalform:  3NF (Dritte Normalform)
-- Tabellen:    5 (USERS, TEAMS, PLAYERS, TOURNAMENTS, MATCHES)
-- ============================================================================

-- Datenbank erstellen (falls nicht vorhanden)
CREATE DATABASE IF NOT EXISTS cs2_esport_db
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_general_ci;

-- Datenbank verwenden
USE cs2_esport_db;

-- ============================================================================
-- TABELLEN LÖSCHEN (in richtiger Reihenfolge wegen Foreign Keys)
-- ============================================================================
SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS MATCHES;
DROP TABLE IF EXISTS TOURNAMENTS;
DROP TABLE IF EXISTS PLAYERS;
DROP TABLE IF EXISTS TEAMS;
DROP TABLE IF EXISTS USERS;
SET FOREIGN_KEY_CHECKS = 1;

-- ============================================================================
-- TABELLE 1: USERS (Benutzer)
-- ============================================================================
-- Beschreibung: Systembenutzer mit Rollen für Zugriffskontrolle
-- Attribute:
--   - user_id:       Primärschlüssel, automatisch inkrementiert
--   - username:      Eindeutiger Benutzername
--   - password_hash: Verschlüsseltes Passwort (bcrypt)
--   - role:          Benutzerrolle (Admin, Manager, Viewer)
--   - email:         E-Mail-Adresse (eindeutig)
--   - created_at:    Erstellungsdatum
--   - last_login:    Letzter Login-Zeitpunkt
-- ============================================================================

CREATE TABLE USERS (
    user_id         INT AUTO_INCREMENT PRIMARY KEY 
                    COMMENT 'Eindeutige User-ID (PK)',
    
    username        VARCHAR(50) UNIQUE NOT NULL 
                    COMMENT 'Benutzername (eindeutig)',
    
    password_hash   VARCHAR(255) NOT NULL 
                    COMMENT 'Verschlüsseltes Passwort (bcrypt)',
    
    role            ENUM('Admin', 'Manager', 'Viewer') NOT NULL DEFAULT 'Viewer' 
                    COMMENT 'Benutzerrolle für Zugriffskontrolle',
    
    email           VARCHAR(100) UNIQUE NOT NULL 
                    COMMENT 'E-Mail-Adresse (eindeutig)',
    
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP 
                    COMMENT 'Erstellungsdatum des Accounts',
    
    last_login      TIMESTAMP NULL 
                    COMMENT 'Zeitpunkt des letzten Logins',
    
    -- Indizes für schnellere Suche
    INDEX idx_users_username (username),
    INDEX idx_users_email (email),
    INDEX idx_users_role (role)
    
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci
COMMENT='Systembenutzer mit Zugriffsrechten';

-- ============================================================================
-- TABELLE 2: TEAMS (CS2 Teams)
-- ============================================================================
-- Beschreibung: Counter-Strike 2 E-Sport Teams
-- Attribute:
--   - team_id:      Primärschlüssel
--   - team_name:    Offizieller Teamname
--   - abbreviation: Kurzform (z.B. NaVi, FaZe)
--   - country:      Herkunftsland
--   - coach:        Name des Coaches
--   - founded_date: Gründungsdatum
--   - created_at:   Erstellungsdatum im System
-- ============================================================================

CREATE TABLE TEAMS (
    team_id         INT AUTO_INCREMENT PRIMARY KEY 
                    COMMENT 'Eindeutige Team-ID (PK)',
    
    team_name       VARCHAR(100) UNIQUE NOT NULL 
                    COMMENT 'Offizieller Teamname',
    
    abbreviation    VARCHAR(10) UNIQUE 
                    COMMENT 'Team-Abkürzung (z.B. NaVi, FaZe)',
    
    country         VARCHAR(50) 
                    COMMENT 'Herkunftsland des Teams',
    
    coach           VARCHAR(100) 
                    COMMENT 'Name des Team-Coaches',
    
    founded_date    DATE 
                    COMMENT 'Gründungsdatum des Teams',
    
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP 
                    COMMENT 'Erstellungsdatum im System',
    
    -- Indizes
    INDEX idx_teams_name (team_name),
    INDEX idx_teams_country (country)
    
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci
COMMENT='CS2 E-Sport Teams';

-- ============================================================================
-- TABELLE 3: PLAYERS (Spieler)
-- ============================================================================
-- Beschreibung: Professionelle CS2 Spieler
-- Attribute:
--   - player_id:    Primärschlüssel
--   - nickname:     In-Game Name (eindeutig)
--   - first_name:   Vorname
--   - last_name:    Nachname
--   - nationality:  Nationalität
--   - role:         Spielerrolle (IGL, AWPer, Entry Fragger, Support, Lurker)
--   - team_id:      Fremdschlüssel zu TEAMS
--   - birth_date:   Geburtsdatum
--   - created_at:   Erstellungsdatum
-- ============================================================================

CREATE TABLE PLAYERS (
    player_id       INT AUTO_INCREMENT PRIMARY KEY 
                    COMMENT 'Eindeutige Spieler-ID (PK)',
    
    nickname        VARCHAR(50) UNIQUE NOT NULL 
                    COMMENT 'In-Game Name des Spielers',
    
    first_name      VARCHAR(50) NOT NULL 
                    COMMENT 'Vorname des Spielers',
    
    last_name       VARCHAR(50) NOT NULL 
                    COMMENT 'Nachname des Spielers',
    
    nationality     VARCHAR(50) 
                    COMMENT 'Nationalität des Spielers',
    
    role            ENUM('IGL', 'AWPer', 'Entry Fragger', 'Support', 'Lurker') 
                    COMMENT 'CS2 Spielerrolle',
    
    team_id         INT 
                    COMMENT 'Fremdschlüssel zu TEAMS',
    
    birth_date      DATE 
                    COMMENT 'Geburtsdatum des Spielers',
    
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP 
                    COMMENT 'Erstellungsdatum im System',
    
    -- Fremdschlüssel-Constraint
    CONSTRAINT fk_players_team 
        FOREIGN KEY (team_id) REFERENCES TEAMS(team_id)
        ON DELETE SET NULL 
        ON UPDATE CASCADE,
    
    -- Indizes
    INDEX idx_players_nickname (nickname),
    INDEX idx_players_team (team_id),
    INDEX idx_players_role (role)
    
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci
COMMENT='CS2 Profispieler';

-- ============================================================================
-- TABELLE 4: TOURNAMENTS (Turniere)
-- ============================================================================
-- Beschreibung: CS2 E-Sport Turniere und Events
-- Attribute:
--   - tournament_id:   Primärschlüssel
--   - tournament_name: Turniername
--   - location:        Austragungsort
--   - start_date:      Startdatum
--   - end_date:        Enddatum
--   - prize_pool:      Preisgeld in USD
--   - tier:            Turnierkategorie (S-Tier, A-Tier, B-Tier, C-Tier)
--   - status:          Status (Upcoming, Ongoing, Completed, Cancelled)
-- ============================================================================

CREATE TABLE TOURNAMENTS (
    tournament_id   INT AUTO_INCREMENT PRIMARY KEY 
                    COMMENT 'Eindeutige Turnier-ID (PK)',
    
    tournament_name VARCHAR(150) NOT NULL 
                    COMMENT 'Offizieller Turniername',
    
    location        VARCHAR(100) 
                    COMMENT 'Austragungsort (Stadt, Land)',
    
    start_date      DATE NOT NULL 
                    COMMENT 'Startdatum des Turniers',
    
    end_date        DATE NOT NULL 
                    COMMENT 'Enddatum des Turniers',
    
    prize_pool      DECIMAL(12, 2) 
                    COMMENT 'Preisgeld in USD',
    
    tier            ENUM('S-Tier', 'A-Tier', 'B-Tier', 'C-Tier') DEFAULT 'B-Tier' 
                    COMMENT 'Turnierkategorie nach HLTV',
    
    status          ENUM('Upcoming', 'Ongoing', 'Completed', 'Cancelled') DEFAULT 'Upcoming' 
                    COMMENT 'Aktueller Turnierstatus',
    
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP 
                    COMMENT 'Erstellungsdatum im System',
    
    -- Constraint: Enddatum >= Startdatum
    CONSTRAINT chk_tournament_dates 
        CHECK (end_date >= start_date),
    
    -- Indizes
    INDEX idx_tournaments_name (tournament_name),
    INDEX idx_tournaments_tier (tier),
    INDEX idx_tournaments_status (status),
    INDEX idx_tournaments_dates (start_date, end_date)
    
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci
COMMENT='CS2 E-Sport Turniere';

-- ============================================================================
-- TABELLE 5: MATCHES (Spiele)
-- ============================================================================
-- Beschreibung: Einzelne Spiele zwischen Teams in Turnieren
-- Attribute:
--   - match_id:       Primärschlüssel
--   - tournament_id:  Fremdschlüssel zu TOURNAMENTS
--   - team1_id:       Fremdschlüssel zu TEAMS (Team 1)
--   - team2_id:       Fremdschlüssel zu TEAMS (Team 2)
--   - score_team1:    Punkte Team 1
--   - score_team2:    Punkte Team 2
--   - match_date:     Datum und Uhrzeit
--   - best_of:        Format (BO1, BO3, BO5)
--   - stage:          Turnierphase
--   - winner_team_id: Fremdschlüssel zu TEAMS (Gewinner)
-- ============================================================================

CREATE TABLE MATCHES (
    match_id        INT AUTO_INCREMENT PRIMARY KEY 
                    COMMENT 'Eindeutige Match-ID (PK)',
    
    tournament_id   INT NOT NULL 
                    COMMENT 'Fremdschlüssel zu TOURNAMENTS',
    
    team1_id        INT NOT NULL 
                    COMMENT 'Fremdschlüssel zu TEAMS (Team 1)',
    
    team2_id        INT NOT NULL 
                    COMMENT 'Fremdschlüssel zu TEAMS (Team 2)',
    
    score_team1     INT DEFAULT 0 
                    COMMENT 'Punkte/Maps von Team 1',
    
    score_team2     INT DEFAULT 0 
                    COMMENT 'Punkte/Maps von Team 2',
    
    match_date      DATETIME NOT NULL 
                    COMMENT 'Datum und Uhrzeit des Matches',
    
    best_of         ENUM('BO1', 'BO3', 'BO5') DEFAULT 'BO3' 
                    COMMENT 'Match-Format',
    
    stage           VARCHAR(50) 
                    COMMENT 'Turnierphase (Group Stage, Playoffs, Final)',
    
    winner_team_id  INT 
                    COMMENT 'Fremdschlüssel zu TEAMS (Gewinner)',
    
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP 
                    COMMENT 'Erstellungsdatum im System',
    
    -- Fremdschlüssel-Constraints
    CONSTRAINT fk_matches_tournament 
        FOREIGN KEY (tournament_id) REFERENCES TOURNAMENTS(tournament_id)
        ON DELETE CASCADE 
        ON UPDATE CASCADE,
    
    CONSTRAINT fk_matches_team1 
        FOREIGN KEY (team1_id) REFERENCES TEAMS(team_id)
        ON DELETE RESTRICT 
        ON UPDATE CASCADE,
    
    CONSTRAINT fk_matches_team2 
        FOREIGN KEY (team2_id) REFERENCES TEAMS(team_id)
        ON DELETE RESTRICT 
        ON UPDATE CASCADE,
    
    CONSTRAINT fk_matches_winner 
        FOREIGN KEY (winner_team_id) REFERENCES TEAMS(team_id)
        ON DELETE SET NULL 
        ON UPDATE CASCADE,
    
    -- Constraint: Team kann nicht gegen sich selbst spielen
    CONSTRAINT chk_different_teams 
        CHECK (team1_id != team2_id),
    
    -- Indizes
    INDEX idx_matches_tournament (tournament_id),
    INDEX idx_matches_teams (team1_id, team2_id),
    INDEX idx_matches_date (match_date),
    INDEX idx_matches_winner (winner_team_id)
    
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci
COMMENT='CS2 E-Sport Matches';

-- ============================================================================
-- BEISPIELDATEN EINFÜGEN
-- ============================================================================

-- Benutzer
INSERT INTO USERS (username, password_hash, role, email) VALUES
('admin', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.rJMi8l7f1F/3m6', 'Admin', 'admin@cs2esport.de'),
('manager', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.rJMi8l7f1F/3m6', 'Manager', 'manager@cs2esport.de'),
('viewer', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.rJMi8l7f1F/3m6', 'Viewer', 'viewer@cs2esport.de');

-- Teams
INSERT INTO TEAMS (team_name, abbreviation, country, coach, founded_date) VALUES
('Natus Vincere', 'NaVi', 'Ukraine', 'Andrii Gorodenskyi', '2009-12-17'),
('FaZe Clan', 'FaZe', 'USA', 'Filip Kubski', '2016-01-20'),
('G2 Esports', 'G2', 'Germany', 'Remy Quoniam', '2014-02-24'),
('Team Vitality', 'VIT', 'France', 'Rémy Aumaitre', '2013-08-01');

-- Spieler
INSERT INTO PLAYERS (nickname, first_name, last_name, nationality, role, team_id, birth_date) VALUES
('s1mple', 'Oleksandr', 'Kostyliev', 'Ukraine', 'AWPer', 1, '1997-10-02'),
('b1t', 'Valeriy', 'Vakhovskyi', 'Ukraine', 'Entry Fragger', 1, '2003-01-05'),
('jL', 'Justinas', 'Lekavicius', 'Lithuania', 'IGL', 1, '1999-03-29'),
('karrigan', 'Finn', 'Andersen', 'Denmark', 'IGL', 2, '1990-04-14'),
('ropz', 'Robin', 'Kool', 'Estonia', 'Lurker', 2, '1999-12-22'),
('broky', 'Helvijs', 'Saukants', 'Latvia', 'AWPer', 2, '2002-08-14'),
('NiKo', 'Nikola', 'Kovac', 'Bosnia', 'Entry Fragger', 3, '1997-02-16'),
('m0NESY', 'Ilya', 'Osipov', 'Russia', 'AWPer', 3, '2005-05-01'),
('ZywOo', 'Mathieu', 'Herbaut', 'France', 'AWPer', 4, '2000-11-09'),
('apEX', 'Dan', 'Madesclaire', 'France', 'IGL', 4, '1993-02-22');

-- Turniere
INSERT INTO TOURNAMENTS (tournament_name, location, start_date, end_date, prize_pool, tier, status) VALUES
('BLAST Premier 2025', 'Abu Dhabi, UAE', '2025-01-22', '2025-01-26', 1000000.00, 'S-Tier', 'Upcoming'),
('IEM Katowice 2025', 'Katowice, Poland', '2025-02-01', '2025-02-09', 1000000.00, 'S-Tier', 'Upcoming'),
('PGL Major Copenhagen 2024', 'Copenhagen, Denmark', '2024-03-17', '2024-03-31', 1250000.00, 'S-Tier', 'Completed'),
('ESL Pro League S19', 'Malta', '2024-04-02', '2024-04-14', 850000.00, 'A-Tier', 'Completed');

-- Matches
INSERT INTO MATCHES (tournament_id, team1_id, team2_id, score_team1, score_team2, match_date, best_of, stage, winner_team_id) VALUES
(3, 1, 2, 2, 1, '2024-03-31 18:00:00', 'BO5', 'Grand Final', 1),
(3, 1, 3, 2, 0, '2024-03-30 15:00:00', 'BO3', 'Semi-Final', 1),
(3, 2, 4, 2, 1, '2024-03-30 12:00:00', 'BO3', 'Semi-Final', 2),
(4, 3, 4, 2, 1, '2024-04-14 17:00:00', 'BO5', 'Grand Final', 3),
(4, 1, 2, 1, 2, '2024-04-13 15:00:00', 'BO3', 'Semi-Final', 2);

-- ============================================================================
-- VIEWS FÜR HÄUFIGE ABFRAGEN
-- ============================================================================

-- View: Spieler mit Teamnamen
CREATE OR REPLACE VIEW v_players_with_teams AS
SELECT 
    p.player_id,
    p.nickname,
    CONCAT(p.first_name, ' ', p.last_name) AS real_name,
    p.nationality,
    p.role,
    p.birth_date,
    TIMESTAMPDIFF(YEAR, p.birth_date, CURDATE()) AS age,
    t.team_name,
    t.abbreviation AS team_abbr
FROM PLAYERS p
LEFT JOIN TEAMS t ON p.team_id = t.team_id;

-- View: Matches mit Teamnamen
CREATE OR REPLACE VIEW v_matches_detailed AS
SELECT 
    m.match_id,
    trn.tournament_name,
    trn.tier,
    t1.team_name AS team1_name,
    t1.abbreviation AS team1_abbr,
    t2.team_name AS team2_name,
    t2.abbreviation AS team2_abbr,
    m.score_team1,
    m.score_team2,
    CONCAT(m.score_team1, ' : ', m.score_team2) AS score,
    m.match_date,
    m.best_of,
    m.stage,
    tw.team_name AS winner_name
FROM MATCHES m
JOIN TOURNAMENTS trn ON m.tournament_id = trn.tournament_id
JOIN TEAMS t1 ON m.team1_id = t1.team_id
JOIN TEAMS t2 ON m.team2_id = t2.team_id
LEFT JOIN TEAMS tw ON m.winner_team_id = tw.team_id;

-- View: Team-Statistiken
CREATE OR REPLACE VIEW v_team_stats AS
SELECT 
    t.team_id,
    t.team_name,
    t.abbreviation,
    COUNT(DISTINCT p.player_id) AS player_count,
    (SELECT COUNT(*) FROM MATCHES m WHERE m.winner_team_id = t.team_id) AS total_wins
FROM TEAMS t
LEFT JOIN PLAYERS p ON t.team_id = p.team_id
GROUP BY t.team_id, t.team_name, t.abbreviation;

-- ============================================================================
-- SCHEMA VOLLSTÄNDIG ERSTELLT
-- ============================================================================

SELECT '✅ Schema erfolgreich erstellt!' AS Status;

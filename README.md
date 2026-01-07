# CS2 E-Sport Management System

## BTS Datenbankprojekt - Januar 2025

Ein Verwaltungssystem für CS2 E-Sport Organisationen mit MariaDB/MySQL Backend.

---

## 🎯 Projektübersicht

**Kunde:** E-Sport Organisation  
**Datenbank:** MariaDB / MySQL  
**Sprache:** Python 3.10+  
**Normalform:** 3NF (Dritte Normalform)

### Funktionen

- ✅ CRUD-Operationen (Create, Read, Update, Delete)
- ✅ Datenbankverbindung zu MariaDB/MySQL
- ✅ Suche nach Daten
- ✅ Export nach JSON und CSV
- ✅ Import von JSON und CSV
- ✅ Intuitive Menüführung

---

## 📊 Datenbankmodell

### Entitäten (5 Tabellen)

| Tabelle | Beschreibung | Beziehungen |
|---------|--------------|-------------|
| USERS | Systembenutzer | - |
| TEAMS | CS2 Teams | - |
| PLAYERS | Profispieler | → TEAMS |
| TOURNAMENTS | Turniere | - |
| MATCHES | Spiele | → TOURNAMENTS, TEAMS |

### ERD-Beziehungen

```
USERS (keine FK)

TEAMS (keine FK)
  ↑
  │ 1:N
  │
PLAYERS (team_id → TEAMS)

TOURNAMENTS (keine FK)
  ↑
  │ 1:N
  │
MATCHES (tournament_id → TOURNAMENTS)
        (team1_id → TEAMS)
        (team2_id → TEAMS)
        (winner_team_id → TEAMS)
```

---

## 🚀 Installation

### 1. Voraussetzungen

- Python 3.10+
- MariaDB oder MySQL
- XAMPP (empfohlen für lokale Entwicklung)

### 2. Abhängigkeiten installieren

```bash
pip install -r requirements.txt
```

### 3. Datenbank einrichten

```bash
# In phpMyAdmin oder MySQL CLI:
mysql -u root < database/schema.sql
```

### 4. Konfiguration

```bash
# .env.example kopieren
cp .env.example .env

# .env bearbeiten:
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=
DB_NAME=cs2_esport_db
```

### 5. Programm starten

```bash
python src/main.py
```

---

## 📁 Projektstruktur

```
cs2_esport_project/
├── database/
│   └── schema.sql        # SQL-Schema (3NF)
├── src/
│   └── main.py           # Hauptprogramm
├── data/
│   ├── export/           # Exportierte Dateien
│   └── import/           # Zu importierende Dateien
├── docs/                  # Dokumentation
├── .env.example          # Konfigurationsvorlage
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 💻 Programmfeatures

### Hauptmenü

1. **Teams verwalten** - Hinzufügen, Bearbeiten, Löschen
2. **Spieler verwalten** - Mit Teamzuordnung und Rollen
3. **Turniere verwalten** - S-Tier bis C-Tier
4. **Matches verwalten** - Ergebnisse eintragen
5. **Benutzer verwalten** - Admin, Manager, Viewer
6. **Suchen** - Flexible Suchfunktion
7. **Export** - JSON/CSV Export
8. **Import** - JSON/CSV Import
9. **Statistiken** - Übersicht

### Spielerrollen

- IGL (In-Game Leader)
- AWPer
- Entry Fragger
- Support
- Lurker

### Turnier-Tiers

- S-Tier (Majors)
- A-Tier
- B-Tier
- C-Tier

---

## 📝 Technische Details

### 3. Normalform (3NF)

Das Schema erfüllt die 3NF:

1. **1NF:** Alle Attribute sind atomar
2. **2NF:** Keine partiellen Abhängigkeiten (einzelne PKs)
3. **3NF:** Keine transitiven Abhängigkeiten

### Referentielle Integrität

- Foreign Keys mit ON DELETE/UPDATE Aktionen
- RESTRICT verhindert Löschen bei Abhängigkeiten
- CASCADE propagiert Änderungen
- SET NULL bei optionalen Beziehungen

---

## 👤 Autor

**Joel** - BTS Datenbankprojekt 2025

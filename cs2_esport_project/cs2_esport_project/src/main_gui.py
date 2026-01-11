#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
==============================================================================
CS2 E-SPORT MANAGEMENT SYSTEM - GUI Version (Tkinter)
==============================================================================
Projekt:     CS2 E-Sport Organisation Management
Autor:       Joel - BTS Datenbankprojekt
Datum:       Januar 2025
Datenbank:   MariaDB / MySQL
Python:      3.10+
GUI:         Tkinter

Beschreibung:
    Grafische Benutzeroberfläche für das CS2 E-Sport Management System.
    Bietet CRUD-Operationen, Suche und Import/Export Funktionalität.
==============================================================================
"""

# ==============================================================================
# IMPORTS - Benötigte Bibliotheken
# ==============================================================================

import os          # Betriebssystem-Funktionen (Umgebungsvariablen lesen)
import sys         # System-Funktionen (Programm beenden)
import json        # JSON-Dateiverarbeitung für Import/Export
import csv         # CSV-Dateiverarbeitung für Import/Export
import tkinter as tk                              # Haupt-GUI-Bibliothek
from tkinter import ttk, messagebox, filedialog  # Zusätzliche Tkinter-Module
from datetime import datetime, date              # Datum/Zeit-Verarbeitung
from decimal import Decimal                      # Präzise Dezimalzahlen (für Preisgelder)
from typing import Optional, List, Dict, Any     # Type Hints für bessere Code-Dokumentation

# MySQL-Connector importieren - wird für Datenbankverbindung benötigt
try:
    import mysql.connector
    from mysql.connector import Error as MySQLError
except ImportError:
    # Fehlermeldung anzeigen wenn MySQL-Connector nicht installiert ist
    messagebox.showerror("Fehler", "mysql-connector-python nicht installiert!\nInstallieren mit: pip install mysql-connector-python")
    sys.exit(1)  # Programm beenden

# python-dotenv für Umgebungsvariablen (optional)
try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None  # Falls nicht installiert, wird None gesetzt


# ==============================================================================
# KONFIGURATIONSKLASSE
# ==============================================================================

class Config:
    """
    Konfigurationsklasse für Datenbankverbindung und Pfade.

    Lädt die Datenbankeinstellungen aus Umgebungsvariablen oder verwendet
    Standardwerte, falls keine Umgebungsvariablen gesetzt sind.

    Attribute:
        DB_HOST (str): Hostname des Datenbankservers (Standard: localhost)
        DB_PORT (int): Port des Datenbankservers (Standard: 3306)
        DB_USER (str): Benutzername für die Datenbank (Standard: root)
        DB_PASSWORD (str): Passwort für die Datenbank (Standard: leer)
        DB_NAME (str): Name der Datenbank (Standard: cs2_esport_db)
    """

    def __init__(self):
        """Initialisiert die Konfiguration und lädt Umgebungsvariablen."""
        # .env-Datei laden falls python-dotenv installiert ist
        if load_dotenv:
            load_dotenv()

        # Datenbankeinstellungen aus Umgebungsvariablen lesen
        # os.getenv('NAME', 'default') gibt 'default' zurück falls NAME nicht existiert
        self.DB_HOST = os.getenv('DB_HOST', 'localhost')
        self.DB_PORT = int(os.getenv('DB_PORT', '3306'))
        self.DB_USER = os.getenv('DB_USER', 'root')
        self.DB_PASSWORD = os.getenv('DB_PASSWORD', '')
        self.DB_NAME = os.getenv('DB_NAME', 'cs2_esport_db')


# ==============================================================================
# DATENBANKKLASSE
# ==============================================================================

class Database:
    """
    Datenbankklasse für MySQL/MariaDB Verbindung.

    Verwaltet die Verbindung zur Datenbank und führt SQL-Abfragen aus.
    Verwendet parametrisierte Abfragen zum Schutz vor SQL-Injection.

    Attribute:
        config (Config): Konfigurationsobjekt mit Datenbankeinstellungen
        connection: MySQL-Verbindungsobjekt
        cursor: Datenbank-Cursor für SQL-Abfragen
    """

    def __init__(self, config: Config):
        """
        Initialisiert die Datenbankklasse.

        Args:
            config (Config): Konfigurationsobjekt mit Verbindungsdaten
        """
        self.config = config
        self.connection = None  # Verbindung wird erst bei connect() hergestellt
        self.cursor = None      # Cursor wird erst bei connect() erstellt

    def connect(self) -> bool:
        """
        Stellt die Verbindung zur Datenbank her.

        Returns:
            bool: True bei erfolgreicher Verbindung, False bei Fehler
        """
        try:
            # Verbindung mit den Konfigurationsdaten herstellen
            self.connection = mysql.connector.connect(
                host=self.config.DB_HOST,
                port=self.config.DB_PORT,
                user=self.config.DB_USER,
                password=self.config.DB_PASSWORD,
                database=self.config.DB_NAME,
                charset='utf8mb4',                    # Unicode-Unterstützung
                collation='utf8mb4_general_ci'        # Sortierung für Unicode
            )
            # Cursor erstellen - dictionary=True gibt Ergebnisse als Dict zurück
            self.cursor = self.connection.cursor(dictionary=True)
            return True
        except MySQLError as e:
            # Fehlerdialog anzeigen bei Verbindungsproblemen
            messagebox.showerror("Datenbankfehler", f"Verbindung fehlgeschlagen:\n{e}")
            return False

    def disconnect(self):
        """
        Trennt die Datenbankverbindung sauber.
        Schließt erst den Cursor, dann die Verbindung.
        """
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

    def execute(self, query: str, params: tuple = None) -> Optional[List[Dict]]:
        """
        Führt eine SQL-Abfrage aus.

        Args:
            query (str): SQL-Abfrage (kann Platzhalter %s enthalten)
            params (tuple): Parameter für die Platzhalter (optional)

        Returns:
            Optional[List[Dict]]:
                - Bei SELECT: Liste von Dictionaries mit den Ergebnissen
                - Bei INSERT/UPDATE/DELETE: None
                - Bei Fehler: None

        Beispiel:
            # SELECT-Abfrage
            results = db.execute("SELECT * FROM TEAMS WHERE country = %s", ("Germany",))

            # INSERT-Abfrage
            db.execute("INSERT INTO TEAMS (team_name) VALUES (%s)", ("Neues Team",))
        """
        try:
            # Abfrage mit Parametern ausführen (schützt vor SQL-Injection)
            self.cursor.execute(query, params or ())

            # Bei SELECT-Abfragen: Ergebnisse zurückgeben
            if query.strip().upper().startswith('SELECT'):
                return self.cursor.fetchall()

            # Bei anderen Abfragen (INSERT, UPDATE, DELETE): Änderungen speichern
            self.connection.commit()
            return None
        except MySQLError as e:
            # Fehlerdialog anzeigen und Transaktion zurückrollen
            messagebox.showerror("SQL-Fehler", str(e))
            self.connection.rollback()
            return None


# ==============================================================================
# HAUPTANWENDUNGSKLASSE
# ==============================================================================

class CS2EsportApp:
    """
    Hauptanwendungsklasse für das CS2 E-Sport Management System.

    Diese Klasse erstellt und verwaltet die gesamte grafische Benutzeroberfläche.
    Sie enthält alle Funktionen für:
    - Navigation zwischen verschiedenen Tabellen
    - CRUD-Operationen (Create, Read, Update, Delete)
    - Suche in den Daten
    - Import/Export von Daten (JSON, CSV)
    - Statistik-Anzeige

    Attribute:
        root (tk.Tk): Hauptfenster der Anwendung
        config (Config): Konfigurationsobjekt
        db (Database): Datenbankobjekt
        tables (dict): Konfiguration aller Tabellen
        current_table (str): Aktuell ausgewählte Tabelle
        selected_match_id (int): ID des ausgewählten Matches (für Match-Ansicht)
        teams_cache (list): Zwischengespeicherte Team-Daten für Dropdowns
        tournaments_cache (list): Zwischengespeicherte Turnier-Daten für Dropdowns
    """

    def __init__(self, root: tk.Tk):
        """
        Initialisiert die Hauptanwendung.

        Erstellt das Hauptfenster, stellt die Datenbankverbindung her,
        und baut die gesamte Benutzeroberfläche auf.

        Args:
            root (tk.Tk): Das Tkinter-Hauptfenster
        """
        # Hauptfenster speichern und konfigurieren
        self.root = root
        self.root.title("CS2 E-Sport Management System")  # Fenstertitel
        self.root.geometry("1200x700")                    # Startgröße
        self.root.minsize(1000, 600)                      # Minimale Größe

        # ===== DATENBANKVERBINDUNG =====
        # Konfiguration laden und Datenbank verbinden
        self.config = Config()
        self.db = Database(self.config)

        # Bei Verbindungsfehler: Fenster schließen und beenden
        if not self.db.connect():
            self.root.destroy()
            return

        # ===== TABELLENKONFIGURATION =====
        # Dictionary mit allen Tabellen und deren Einstellungen
        # Jede Tabelle hat: Name, Primary Key, Anzeigefeld, Spalten, Formularfelder
        self.tables = {
            # ----- USERS Tabelle -----
            'users': {
                'name': 'USERS',                    # SQL-Tabellenname
                'pk': 'user_id',                    # Primary Key Spalte
                'display_name': 'Benutzer',         # Anzeigename in der GUI
                'columns': ['user_id', 'username', 'role', 'email', 'created_at'],  # Anzuzeigende Spalten
                'headers': ['ID', 'Benutzername', 'Rolle', 'E-Mail', 'Erstellt'],    # Spaltenüberschriften
                'form_fields': [                    # Felder im Hinzufügen/Bearbeiten-Dialog
                    ('username', 'Benutzername', 'entry'),                           # (DB-Feld, Label, Typ)
                    ('password_hash', 'Passwort', 'entry'),
                    ('role', 'Rolle', 'combo', ['Admin', 'Manager', 'Viewer']),      # combo = Dropdown
                    ('email', 'E-Mail', 'entry')
                ]
            },
            # ----- TEAMS Tabelle -----
            'teams': {
                'name': 'TEAMS',
                'pk': 'team_id',
                'display_name': 'Teams',
                'columns': ['team_id', 'team_name', 'abbreviation', 'country', 'coach'],
                'headers': ['ID', 'Teamname', 'Kürzel', 'Land', 'Coach'],
                'form_fields': [
                    ('team_name', 'Teamname', 'entry'),
                    ('abbreviation', 'Kürzel', 'entry'),
                    ('country', 'Land', 'entry'),
                    ('coach', 'Coach', 'entry'),
                    ('founded_date', 'Gründungsdatum (YYYY-MM-DD)', 'entry')
                ]
            },
            # ----- PLAYERS Tabelle -----
            'players': {
                'name': 'PLAYERS',
                'pk': 'player_id',
                'display_name': 'Spieler',
                'columns': ['player_id', 'nickname', 'first_name', 'last_name', 'role', 'team_name'],
                'headers': ['ID', 'Nickname', 'Vorname', 'Nachname', 'Rolle', 'Team'],
                'form_fields': [
                    ('nickname', 'Nickname', 'entry'),
                    ('first_name', 'Vorname', 'entry'),
                    ('last_name', 'Nachname', 'entry'),
                    ('nationality', 'Nationalität', 'entry'),
                    ('role', 'Rolle', 'combo', ['IGL', 'AWPer', 'Entry Fragger', 'Support', 'Lurker']),
                    ('team_id', 'Team', 'team_combo'),      # team_combo = Dropdown mit Teams
                    ('birth_date', 'Geburtsdatum (YYYY-MM-DD)', 'entry')
                ]
            },
            # ----- TOURNAMENTS Tabelle -----
            'tournaments': {
                'name': 'TOURNAMENTS',
                'pk': 'tournament_id',
                'display_name': 'Turniere',
                'columns': ['tournament_id', 'tournament_name', 'location', 'tier', 'status', 'prize_pool'],
                'headers': ['ID', 'Turniername', 'Ort', 'Tier', 'Status', 'Preisgeld'],
                'form_fields': [
                    ('tournament_name', 'Turniername', 'entry'),
                    ('location', 'Ort', 'entry'),
                    ('start_date', 'Startdatum (YYYY-MM-DD)', 'entry'),
                    ('end_date', 'Enddatum (YYYY-MM-DD)', 'entry'),
                    ('prize_pool', 'Preisgeld ($)', 'entry'),
                    ('tier', 'Tier', 'combo', ['S-Tier', 'A-Tier', 'B-Tier', 'C-Tier']),
                    ('status', 'Status', 'combo', ['Upcoming', 'Ongoing', 'Completed', 'Cancelled'])
                ]
            },
            # ----- MATCHES Tabelle -----
            'matches': {
                'name': 'MATCHES',
                'pk': 'match_id',
                'display_name': 'Matches',
                'columns': ['match_id', 'tournament_name', 'matchup', 'score', 'best_of', 'stage', 'match_date'],
                'headers': ['ID', 'Turnier', 'Match', 'Ergebnis', 'Format', 'Phase', 'Datum'],
                'form_fields': [
                    ('tournament_id', 'Turnier', 'tournament_combo'),  # tournament_combo = Dropdown mit Turnieren
                    ('team1_id', 'Team 1', 'team_combo'),
                    ('team2_id', 'Team 2', 'team_combo'),
                    ('score_team1', 'Score Team 1', 'entry'),
                    ('score_team2', 'Score Team 2', 'entry'),
                    ('match_date', 'Datum/Zeit (YYYY-MM-DD HH:MM)', 'entry'),
                    ('best_of', 'Format', 'combo', ['BO1', 'BO3', 'BO5']),
                    ('stage', 'Phase', 'combo', ['Group Stage', 'Quarter-Final', 'Semi-Final', 'Grand Final']),
                    ('winner_team_id', 'Gewinner', 'team_combo_optional')  # Optional: kann leer sein
                ]
            }
        }

        # ===== ZUSTANDSVARIABLEN =====
        self.current_table = 'teams'       # Startet mit Teams-Ansicht
        self.selected_match_id = None      # Kein Match ausgewählt

        # ===== CACHES FÜR DROPDOWNS =====
        # Diese Listen werden für die Dropdown-Menüs in Formularen verwendet
        self.teams_cache = []
        self.tournaments_cache = []
        self.refresh_caches()  # Caches initial füllen

        # ===== UI AUFBAUEN =====
        self.setup_styles()      # Farben und Styles konfigurieren
        self.create_menu()       # Menüleiste erstellen
        self.create_sidebar()    # Seitenleiste mit Navigation erstellen
        self.create_main_area()  # Hauptbereich erstellen
        self.load_data()         # Daten in die Tabelle laden

        # Event-Handler für Fenster schließen
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    # ==========================================================================
    # CACHE-VERWALTUNG
    # ==========================================================================

    def refresh_caches(self):
        """
        Aktualisiert die Caches für Team- und Turnier-Dropdowns.

        Diese Methode wird aufgerufen, wenn Teams oder Turniere hinzugefügt,
        bearbeitet oder gelöscht werden, damit die Dropdown-Menüs aktuell bleiben.
        """
        # Teams aus der Datenbank laden und cachen
        teams = self.db.execute("SELECT team_id, team_name, abbreviation FROM TEAMS ORDER BY team_name")
        self.teams_cache = teams if teams else []

        # Turniere aus der Datenbank laden und cachen
        tournaments = self.db.execute("SELECT tournament_id, tournament_name FROM TOURNAMENTS ORDER BY tournament_name")
        self.tournaments_cache = tournaments if tournaments else []

    # ==========================================================================
    # STYLE-KONFIGURATION
    # ==========================================================================

    def setup_styles(self):
        """
        Konfiguriert das visuelle Styling der Anwendung.

        Definiert das Farbschema (Gaming-Ästhetik mit dunklen Farben)
        und konfiguriert das Aussehen der Treeview-Tabellen.
        """
        # TTK-Style-Objekt erstellen und Theme setzen
        style = ttk.Style()
        style.theme_use('clam')  # 'clam' Theme als Basis

        # ===== FARBSCHEMA (Gaming-Ästhetik) =====
        # Dictionary mit allen verwendeten Farben
        self.colors = {
            'bg_dark': '#1a1a2e',       # Dunkler Hintergrund (Sidebar)
            'bg_medium': '#16213e',     # Mittlerer Hintergrund (Hauptbereich)
            'bg_light': '#0f3460',      # Heller Hintergrund (Buttons, Karten)
            'accent': '#e94560',        # Akzentfarbe (Rot/Pink)
            'accent_green': '#27ae60',  # Grün für Erfolg/Import
            'accent_blue': '#3498db',   # Blau für Export
            'text': '#ffffff',          # Weißer Text
            'text_dim': '#a0a0a0',      # Gedimmter Text (Beschreibungen)
            'gold': '#f1c40f',          # Gold (S-Tier Turniere)
            'silver': '#bdc3c7'         # Silber (A-Tier Turniere)
        }

        # ===== TREEVIEW STYLING =====
        # Konfiguration für die Tabellen-Ansicht
        style.configure("Treeview",
                       background="#2a2a4a",       # Hintergrundfarbe der Zeilen
                       foreground="white",         # Textfarbe
                       fieldbackground="#2a2a4a",  # Hintergrund des leeren Bereichs
                       rowheight=35)               # Zeilenhöhe in Pixel

        # Konfiguration für die Tabellenüberschriften
        style.configure("Treeview.Heading",
                       background="#1a1a2e",
                       foreground="white",
                       font=('Segoe UI', 10, 'bold'))

        # Konfiguration für ausgewählte Zeilen
        style.map("Treeview", background=[('selected', '#e94560')])  # Rot bei Auswahl

    # ==========================================================================
    # MENÜLEISTE
    # ==========================================================================

    def create_menu(self):
        """
        Erstellt die Menüleiste am oberen Fensterrand.

        Enthält drei Menüs:
        - Datei: Export/Import und Beenden
        - Bearbeiten: CRUD-Operationen und Aktualisieren
        - Hilfe: Über-Dialog
        """
        # Hauptmenüleiste erstellen
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # ----- DATEI-MENÜ -----
        file_menu = tk.Menu(menubar, tearoff=0)  # tearoff=0 verhindert "abreißbare" Menüs
        menubar.add_cascade(label="Datei", menu=file_menu)
        file_menu.add_command(label="Export JSON...", command=self.export_json)
        file_menu.add_command(label="Export CSV...", command=self.export_csv)
        file_menu.add_separator()  # Trennlinie
        file_menu.add_command(label="Import JSON...", command=self.import_json)
        file_menu.add_command(label="Import CSV...", command=self.import_csv)
        file_menu.add_separator()
        file_menu.add_command(label="Beenden", command=self.on_closing)

        # ----- BEARBEITEN-MENÜ -----
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Bearbeiten", menu=edit_menu)
        edit_menu.add_command(label="Neu hinzufügen", command=self.add_record)
        edit_menu.add_command(label="Bearbeiten", command=self.edit_record)
        edit_menu.add_command(label="Löschen", command=self.delete_record)
        edit_menu.add_separator()
        edit_menu.add_command(label="Aktualisieren", command=self.refresh_view)

        # ----- HILFE-MENÜ -----
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Hilfe", menu=help_menu)
        help_menu.add_command(label="Über", command=self.show_about)

    # ==========================================================================
    # SEITENLEISTE (NAVIGATION)
    # ==========================================================================

    def create_sidebar(self):
        """
        Erstellt die Seitenleiste mit Navigation.

        Die Seitenleiste enthält:
        - Logo und Titel
        - Navigationsbuttons für jede Tabelle
        - Statistik-Button am unteren Rand
        """
        # Container für die Seitenleiste erstellen
        self.sidebar = tk.Frame(self.root, bg=self.colors['bg_dark'], width=200)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar.pack_propagate(False)  # Verhindert, dass sich die Breite anpasst

        # ----- LOGO/TITEL -----
        title_frame = tk.Frame(self.sidebar, bg=self.colors['bg_dark'])
        title_frame.pack(fill=tk.X, pady=20)

        # Haupttitel mit Gaming-Emoji
        tk.Label(title_frame, text="🎮 CS2 E-Sport",
                font=('Segoe UI', 16, 'bold'),
                bg=self.colors['bg_dark'],
                fg=self.colors['accent']).pack()

        # Untertitel
        tk.Label(title_frame, text="Management System",
                font=('Segoe UI', 10),
                bg=self.colors['bg_dark'],
                fg=self.colors['text_dim']).pack()

        # ----- TRENNLINIE -----
        tk.Frame(self.sidebar, height=2, bg=self.colors['bg_light']).pack(fill=tk.X, padx=15, pady=10)

        # ----- NAVIGATIONSBUTTONS -----
        # Liste der Navigationselemente: (Anzeige-Text, Tabellen-Key)
        nav_items = [
            ('🏆 Teams', 'teams'),
            ('👤 Spieler', 'players'),
            ('🎯 Turniere', 'tournaments'),
            ('⚔️ Matches', 'matches'),
            ('👥 Benutzer', 'users')
        ]

        # Dictionary zum Speichern der Button-Referenzen (für Highlighting)
        self.nav_buttons = {}

        # Buttons erstellen
        for text, table_key in nav_items:
            btn = tk.Button(self.sidebar, text=text,
                           font=('Segoe UI', 11),
                           bg=self.colors['bg_medium'],
                           fg=self.colors['text'],
                           activebackground=self.colors['accent'],
                           relief=tk.FLAT,        # Flacher Button ohne Rahmen
                           anchor='w',            # Text links ausrichten
                           padx=20,
                           pady=12,
                           cursor='hand2',        # Hand-Cursor bei Hover
                           command=lambda t=table_key: self.switch_table(t))  # Lambda für Tabellenwechsel
            btn.pack(fill=tk.X, padx=10, pady=2)
            self.nav_buttons[table_key] = btn

            # Hover-Effekte hinzufügen
            btn.bind('<Enter>', lambda e, b=btn: b.config(bg=self.colors['bg_light']))  # Maus rein
            btn.bind('<Leave>', lambda e, b=btn, t=table_key: self.update_button_color(b, t))  # Maus raus

        # Initiales Highlighting setzen
        self.update_nav_highlight()

        # ----- STATISTIK-BUTTON (unten) -----
        stats_frame = tk.Frame(self.sidebar, bg=self.colors['bg_dark'])
        stats_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=20)

        tk.Button(stats_frame, text="📊 Statistiken",
                 font=('Segoe UI', 10),
                 bg=self.colors['accent'],
                 fg='white',
                 relief=tk.FLAT,
                 padx=20, pady=10,
                 cursor='hand2',
                 command=self.show_statistics).pack(fill=tk.X, padx=10)

    def update_button_color(self, btn, table_key):
        """
        Aktualisiert die Buttonfarbe basierend auf der aktuellen Auswahl.

        Wird beim Mouse-Leave-Event aufgerufen, um sicherzustellen,
        dass der aktive Button hervorgehoben bleibt.

        Args:
            btn: Der Button, dessen Farbe aktualisiert werden soll
            table_key (str): Der Tabellen-Key des Buttons
        """
        if table_key == self.current_table:
            btn.config(bg=self.colors['accent'])  # Aktiver Button = Akzentfarbe
        else:
            btn.config(bg=self.colors['bg_medium'])  # Inaktiver Button = normale Farbe

    def update_nav_highlight(self):
        """
        Aktualisiert die Hervorhebung des aktiven Navigationsbuttons.

        Geht durch alle Buttons und setzt die Farbe entsprechend
        der aktuell ausgewählten Tabelle.
        """
        for key, btn in self.nav_buttons.items():
            if key == self.current_table:
                btn.config(bg=self.colors['accent'])  # Akzentfarbe für aktiven Button
            else:
                btn.config(bg=self.colors['bg_medium'])  # Normale Farbe für andere

    def switch_table(self, table_key: str):
        """
        Wechselt zur angegebenen Tabelle.

        Aktualisiert die Navigation, lädt die Daten der neuen Tabelle
        und zeigt die entsprechende Ansicht an.

        Args:
            table_key (str): Der Key der Tabelle (z.B. 'teams', 'players')
        """
        # Zustand aktualisieren
        self.current_table = table_key
        self.selected_match_id = None  # Match-Auswahl zurücksetzen

        # UI aktualisieren
        self.update_nav_highlight()
        self.update_table_header()
        self.refresh_caches()  # Caches für Dropdowns aktualisieren

        # Entsprechende Ansicht anzeigen
        if table_key == 'matches':
            self.show_matches_view()  # Spezielle Karten-Ansicht für Matches
        else:
            self.show_table_view()    # Normale Tabellen-Ansicht
            self.load_data()

    # ==========================================================================
    # HAUPTBEREICH
    # ==========================================================================

    def create_main_area(self):
        """
        Erstellt den Hauptbereich der Anwendung.

        Der Hauptbereich enthält:
        - Header mit Titel und CRUD-Buttons
        - Suchleiste
        - Tabellen-/Karten-Ansicht
        - Statusleiste am unteren Rand
        """
        # Container für den Hauptbereich
        self.main_frame = tk.Frame(self.root, bg=self.colors['bg_medium'])
        self.main_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # ===== HEADER MIT TITEL UND BUTTONS =====
        self.header_frame = tk.Frame(self.main_frame, bg=self.colors['bg_medium'])
        self.header_frame.pack(fill=tk.X, padx=20, pady=15)

        # Titel (links im Header)
        self.header_label = tk.Label(self.header_frame,
                                     text="🏆 Teams",
                                     font=('Segoe UI', 20, 'bold'),
                                     bg=self.colors['bg_medium'],
                                     fg='white')
        self.header_label.pack(side=tk.LEFT)

        # Button-Container (rechts im Header)
        btn_frame = tk.Frame(self.header_frame, bg=self.colors['bg_medium'])
        btn_frame.pack(side=tk.RIGHT)

        # ----- CRUD BUTTONS -----
        # Hinzufügen-Button (Akzentfarbe)
        tk.Button(btn_frame, text="➕ Hinzufügen",
                 font=('Segoe UI', 10),
                 bg=self.colors['accent'],
                 fg='white',
                 relief=tk.FLAT,
                 padx=12, pady=8,
                 cursor='hand2',
                 command=self.add_record).pack(side=tk.LEFT, padx=3)

        # Bearbeiten-Button
        tk.Button(btn_frame, text="✏️ Bearbeiten",
                 font=('Segoe UI', 10),
                 bg=self.colors['bg_light'],
                 fg='white',
                 relief=tk.FLAT,
                 padx=12, pady=8,
                 cursor='hand2',
                 command=self.edit_record).pack(side=tk.LEFT, padx=3)

        # Löschen-Button (Rot für Gefahr)
        tk.Button(btn_frame, text="🗑️ Löschen",
                 font=('Segoe UI', 10),
                 bg='#c0392b',  # Dunkelrot
                 fg='white',
                 relief=tk.FLAT,
                 padx=12, pady=8,
                 cursor='hand2',
                 command=self.delete_record).pack(side=tk.LEFT, padx=3)

        # ----- VERTIKALER SEPARATOR -----
        separator = tk.Frame(btn_frame, width=2, bg=self.colors['bg_light'])
        separator.pack(side=tk.LEFT, padx=10, fill=tk.Y, pady=5)

        # ----- IMPORT/EXPORT BUTTONS -----
        # Import-Button (Grün)
        tk.Button(btn_frame, text="📥 Import",
                 font=('Segoe UI', 10),
                 bg=self.colors['accent_green'],
                 fg='white',
                 relief=tk.FLAT,
                 padx=12, pady=8,
                 cursor='hand2',
                 command=self.show_import_dialog).pack(side=tk.LEFT, padx=3)

        # Export-Button (Blau)
        tk.Button(btn_frame, text="📤 Export",
                 font=('Segoe UI', 10),
                 bg=self.colors['accent_blue'],
                 fg='white',
                 relief=tk.FLAT,
                 padx=12, pady=8,
                 cursor='hand2',
                 command=self.show_export_dialog).pack(side=tk.LEFT, padx=3)

        # ===== SUCHLEISTE =====
        search_frame = tk.Frame(self.main_frame, bg=self.colors['bg_medium'])
        search_frame.pack(fill=tk.X, padx=20, pady=(0, 10))

        # Such-Icon
        tk.Label(search_frame, text="🔍",
                font=('Segoe UI', 12),
                bg=self.colors['bg_medium'],
                fg='white').pack(side=tk.LEFT)

        # Such-Eingabefeld
        self.search_var = tk.StringVar()  # Variable zum Speichern des Suchtexts
        self.search_var.trace('w', self.on_search)  # Bei Änderung on_search aufrufen
        search_entry = tk.Entry(search_frame,
                               textvariable=self.search_var,
                               font=('Segoe UI', 11),
                               bg=self.colors['bg_dark'],
                               fg='white',
                               insertbackground='white',  # Cursor-Farbe
                               relief=tk.FLAT,
                               width=40)
        search_entry.pack(side=tk.LEFT, padx=10, ipady=8)

        # ===== CONTENT-BEREICH =====
        self.content_frame = tk.Frame(self.main_frame, bg=self.colors['bg_medium'])
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

        # ----- TABLE CONTAINER (für normale Tabellen) -----
        self.table_container = tk.Frame(self.content_frame, bg=self.colors['bg_medium'])
        self.table_container.pack(fill=tk.BOTH, expand=True)

        # Scrollbars für die Tabelle
        y_scroll = ttk.Scrollbar(self.table_container, orient=tk.VERTICAL)
        y_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        x_scroll = ttk.Scrollbar(self.table_container, orient=tk.HORIZONTAL)
        x_scroll.pack(side=tk.BOTTOM, fill=tk.X)

        # Treeview (Tabelle) erstellen
        self.tree = ttk.Treeview(self.table_container,
                                yscrollcommand=y_scroll.set,
                                xscrollcommand=x_scroll.set,
                                selectmode='browse')  # Nur eine Zeile gleichzeitig auswählbar
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Scrollbars mit Treeview verbinden
        y_scroll.config(command=self.tree.yview)
        x_scroll.config(command=self.tree.xview)

        # Doppelklick zum Bearbeiten
        self.tree.bind('<Double-1>', lambda e: self.edit_record())

        # ----- MATCHES CONTAINER (für Karten-Ansicht) -----
        self.matches_container = tk.Frame(self.content_frame, bg=self.colors['bg_medium'])

        # ===== STATUSLEISTE =====
        self.status_frame = tk.Frame(self.main_frame, bg=self.colors['bg_dark'])
        self.status_frame.pack(fill=tk.X, side=tk.BOTTOM)

        self.status_label = tk.Label(self.status_frame,
                                    text="Bereit",
                                    font=('Segoe UI', 9),
                                    bg=self.colors['bg_dark'],
                                    fg=self.colors['text_dim'],
                                    anchor='w',  # Text links ausrichten
                                    padx=10, pady=5)
        self.status_label.pack(fill=tk.X)

    # ==========================================================================
    # IMPORT/EXPORT DIALOGE
    # ==========================================================================

    def show_import_dialog(self):
        """
        Zeigt Import-Dialog mit Auswahl JSON oder CSV.

        Öffnet ein modales Fenster, in dem der Benutzer das
        gewünschte Import-Format auswählen kann.
        """
        # Modales Dialog-Fenster erstellen
        dialog = tk.Toplevel(self.root)
        dialog.title("Daten importieren")
        dialog.geometry("350x200")
        dialog.resizable(False, False)
        dialog.transient(self.root)  # Über Hauptfenster anzeigen
        dialog.grab_set()            # Fokus auf Dialog beschränken (modal)
        dialog.configure(bg=self.colors['bg_medium'])

        # Dialog zentrieren auf dem Bildschirm
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() - 350) // 2
        y = (dialog.winfo_screenheight() - 200) // 2
        dialog.geometry(f"+{x}+{y}")

        # Titel
        tk.Label(dialog, text="📥 Import Format wählen",
                font=('Segoe UI', 14, 'bold'),
                bg=self.colors['bg_medium'],
                fg='white').pack(pady=20)

        # Info-Text: In welche Tabelle wird importiert
        tk.Label(dialog,
                text=f"Importiere in: {self.tables[self.current_table]['display_name']}",
                font=('Segoe UI', 10),
                bg=self.colors['bg_medium'],
                fg=self.colors['text_dim']).pack()

        # Button-Container
        btn_frame = tk.Frame(dialog, bg=self.colors['bg_medium'])
        btn_frame.pack(pady=25)

        # JSON-Button - schließt Dialog und startet Import
        tk.Button(btn_frame, text="📄 JSON",
                 font=('Segoe UI', 12, 'bold'),
                 bg=self.colors['accent_green'],
                 fg='white',
                 relief=tk.FLAT,
                 padx=30, pady=12,
                 cursor='hand2',
                 command=lambda: [dialog.destroy(), self.import_json()]).pack(side=tk.LEFT, padx=10)

        # CSV-Button - schließt Dialog und startet Import
        tk.Button(btn_frame, text="📊 CSV",
                 font=('Segoe UI', 12, 'bold'),
                 bg=self.colors['accent_blue'],
                 fg='white',
                 relief=tk.FLAT,
                 padx=30, pady=12,
                 cursor='hand2',
                 command=lambda: [dialog.destroy(), self.import_csv()]).pack(side=tk.LEFT, padx=10)

    def show_export_dialog(self):
        """
        Zeigt Export-Dialog mit Auswahl JSON oder CSV.

        Öffnet ein modales Fenster, in dem der Benutzer das
        gewünschte Export-Format auswählen kann.
        """
        # Modales Dialog-Fenster erstellen
        dialog = tk.Toplevel(self.root)
        dialog.title("Daten exportieren")
        dialog.geometry("350x200")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.configure(bg=self.colors['bg_medium'])

        # Dialog zentrieren
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() - 350) // 2
        y = (dialog.winfo_screenheight() - 200) // 2
        dialog.geometry(f"+{x}+{y}")

        # Titel
        tk.Label(dialog, text="📤 Export Format wählen",
                font=('Segoe UI', 14, 'bold'),
                bg=self.colors['bg_medium'],
                fg='white').pack(pady=20)

        # Info-Text: Welche Tabelle wird exportiert
        tk.Label(dialog,
                text=f"Exportiere: {self.tables[self.current_table]['display_name']}",
                font=('Segoe UI', 10),
                bg=self.colors['bg_medium'],
                fg=self.colors['text_dim']).pack()

        # Button-Container
        btn_frame = tk.Frame(dialog, bg=self.colors['bg_medium'])
        btn_frame.pack(pady=25)

        # JSON-Button
        tk.Button(btn_frame, text="📄 JSON",
                 font=('Segoe UI', 12, 'bold'),
                 bg=self.colors['accent_green'],
                 fg='white',
                 relief=tk.FLAT,
                 padx=30, pady=12,
                 cursor='hand2',
                 command=lambda: [dialog.destroy(), self.export_json()]).pack(side=tk.LEFT, padx=10)

        # CSV-Button
        tk.Button(btn_frame, text="📊 CSV",
                 font=('Segoe UI', 12, 'bold'),
                 bg=self.colors['accent_blue'],
                 fg='white',
                 relief=tk.FLAT,
                 padx=30, pady=12,
                 cursor='hand2',
                 command=lambda: [dialog.destroy(), self.export_csv()]).pack(side=tk.LEFT, padx=10)

    # ==========================================================================
    # ANSICHTEN (VIEWS)
    # ==========================================================================

    def show_table_view(self):
        """
        Zeigt die normale Tabellenansicht.

        Versteckt die Match-Karten-Ansicht und zeigt stattdessen
        die Treeview-Tabelle an.
        """
        self.matches_container.pack_forget()  # Karten-Ansicht verstecken
        self.table_container.pack(fill=tk.BOTH, expand=True)  # Tabelle anzeigen

    def show_matches_view(self):
        """
        Zeigt die Match-Karten-Ansicht.

        Spezielle Ansicht für Matches mit Karten statt einer Tabelle.
        Zeigt Matches gruppiert nach Turnieren mit visuellen Karten.
        """
        # Tabellen-Ansicht verstecken
        self.table_container.pack_forget()

        # Alte Widgets aus dem Container entfernen (Canvas, Scrollbar etc.)
        for widget in self.matches_container.winfo_children():
            widget.destroy()

        # Container anzeigen
        self.matches_container.pack(fill=tk.BOTH, expand=True)

        # ===== SCROLLBARER CANVAS =====
        # Canvas ermöglicht Scrolling für viele Match-Karten
        canvas = tk.Canvas(self.matches_container, bg=self.colors['bg_medium'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.matches_container, orient="vertical", command=canvas.yview)
        self.matches_scroll_frame = tk.Frame(canvas, bg=self.colors['bg_medium'])

        # Scroll-Region automatisch anpassen wenn sich Inhalt ändert
        self.matches_scroll_frame.bind("<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        # Frame im Canvas platzieren
        canvas.create_window((0, 0), window=self.matches_scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Mausrad-Scrolling aktivieren
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))

        # Canvas und Scrollbar anzeigen
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Match-Karten laden
        self.load_matches_cards()

    def load_matches_cards(self):
        """
        Lädt und zeigt die Match-Karten.

        Führt eine komplexe SQL-Abfrage aus, um alle Match-Daten
        inklusive Turnier- und Team-Informationen zu laden.
        Gruppiert die Matches nach Turnieren und erstellt visuelle Karten.
        """
        # SQL-Abfrage mit JOINs für vollständige Match-Informationen
        query = """
            SELECT m.match_id, t.tournament_name, t.tier,
                   t1.team_name AS team1_name, t1.abbreviation AS team1_abbr,
                   t2.team_name AS team2_name, t2.abbreviation AS team2_abbr,
                   m.score_team1, m.score_team2, m.match_date, m.best_of, m.stage,
                   m.winner_team_id, t1.team_id AS team1_id, t2.team_id AS team2_id,
                   tw.team_name AS winner_name
            FROM MATCHES m
            JOIN TOURNAMENTS t ON m.tournament_id = t.tournament_id
            JOIN TEAMS t1 ON m.team1_id = t1.team_id
            JOIN TEAMS t2 ON m.team2_id = t2.team_id
            LEFT JOIN TEAMS tw ON m.winner_team_id = tw.team_id
            ORDER BY m.match_date DESC
        """
        matches = self.db.execute(query)

        # Keine Matches vorhanden
        if not matches:
            tk.Label(self.matches_scroll_frame,
                    text="Keine Matches vorhanden",
                    font=('Segoe UI', 14),
                    bg=self.colors['bg_medium'],
                    fg=self.colors['text_dim']).pack(pady=50)
            return

        # ===== MATCHES NACH TURNIER GRUPPIEREN =====
        tournaments = {}
        for match in matches:
            t_name = match['tournament_name']
            if t_name not in tournaments:
                tournaments[t_name] = {'tier': match['tier'], 'matches': []}
            tournaments[t_name]['matches'].append(match)

        # Farben für verschiedene Turnier-Tiers
        tier_colors = {
            'S-Tier': self.colors['gold'],      # Gold für höchste Stufe
            'A-Tier': self.colors['silver'],    # Silber für zweithöchste
            'B-Tier': '#cd7f32',                # Bronze
            'C-Tier': self.colors['text_dim']   # Grau für niedrigste
        }

        # ===== TURNIER-SEKTIONEN ERSTELLEN =====
        for tournament_name, tournament_data in tournaments.items():
            tier_color = tier_colors.get(tournament_data['tier'], self.colors['text_dim'])

            # ----- TURNIER-HEADER -----
            t_frame = tk.Frame(self.matches_scroll_frame, bg=self.colors['bg_dark'])
            t_frame.pack(fill=tk.X, pady=(15, 5), padx=10)

            # Turniername mit Pokal-Emoji
            tk.Label(t_frame, text=f"🏆 {tournament_name}",
                    font=('Segoe UI', 14, 'bold'),
                    bg=self.colors['bg_dark'],
                    fg=tier_color).pack(side=tk.LEFT, padx=15, pady=10)

            # Tier-Badge
            tk.Label(t_frame, text=tournament_data['tier'],
                    font=('Segoe UI', 10),
                    bg=tier_color,
                    fg='black',
                    padx=10, pady=2).pack(side=tk.RIGHT, padx=15, pady=10)

            # ----- MATCH-KARTEN ERSTELLEN -----
            for match in tournament_data['matches']:
                self.create_match_card(match)

        # Statusleiste aktualisieren
        self.status_label.config(text=f"{len(matches)} Matches geladen")

    def create_match_card(self, match: Dict):
        """
        Erstellt eine einzelne Match-Karte.

        Zeigt Match-Informationen in einer visuellen Karte an:
        - Spielphase und Format (links)
        - Team-Namen und Scores (Mitte)
        - Gewinner-Anzeige (rechts)

        Args:
            match (Dict): Dictionary mit Match-Daten aus der Datenbank
        """
        # ===== KARTEN-CONTAINER =====
        card = tk.Frame(self.matches_scroll_frame,
                       bg=self.colors['bg_light'],
                       highlightbackground=self.colors['accent'],  # Rahmenfarbe
                       highlightthickness=1)                       # Rahmendicke
        card.pack(fill=tk.X, padx=20, pady=5)
        card.match_id = match['match_id']  # ID für spätere Referenz speichern

        # ===== CLICK-HANDLER =====
        def on_click(event, m_id=match['match_id']):
            """Einzelklick: Karte auswählen"""
            self.selected_match_id = m_id
            # Alle Karten zurücksetzen (normale Rahmenfarbe)
            for w in self.matches_scroll_frame.winfo_children():
                if hasattr(w, 'match_id'):
                    w.config(highlightbackground=self.colors['accent'], highlightthickness=1)
            # Diese Karte hervorheben (goldener, dickerer Rahmen)
            card.config(highlightbackground=self.colors['gold'], highlightthickness=3)

        def on_double(event, m_id=match['match_id']):
            """Doppelklick: Bearbeiten-Dialog öffnen"""
            self.selected_match_id = m_id
            self.edit_record()

        # Events binden
        card.bind('<Button-1>', on_click)
        card.bind('<Double-1>', on_double)

        # ===== INNERER CONTAINER =====
        inner = tk.Frame(card, bg=self.colors['bg_light'])
        inner.pack(fill=tk.X, padx=15, pady=12)
        inner.bind('<Button-1>', on_click)  # Auch innerer Container reagiert auf Klicks

        # ===== LINKE SEITE: Stage, Format, Datum =====
        left = tk.Frame(inner, bg=self.colors['bg_light'], width=120)
        left.pack(side=tk.LEFT, fill=tk.Y)
        left.pack_propagate(False)  # Feste Breite beibehalten

        # Spielphase (z.B. "Grand Final")
        tk.Label(left, text=match['stage'] or "Match",
                font=('Segoe UI', 9),
                bg=self.colors['bg_light'],
                fg=self.colors['text_dim']).pack(anchor='w')

        # Format (z.B. "BO3")
        tk.Label(left, text=match['best_of'],
                font=('Segoe UI', 10, 'bold'),
                bg=self.colors['bg_light'],
                fg=self.colors['accent']).pack(anchor='w')

        # Datum (falls vorhanden)
        if match['match_date']:
            date_str = match['match_date'].strftime("%d.%m.%Y")
            tk.Label(left, text=date_str,
                    font=('Segoe UI', 8),
                    bg=self.colors['bg_light'],
                    fg=self.colors['text_dim']).pack(anchor='w', pady=(5, 0))

        # ===== MITTE: Teams und Score =====
        center = tk.Frame(inner, bg=self.colors['bg_light'])
        center.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=20)

        # ----- TEAM 1 -----
        t1_win = match['winner_team_id'] == match['team1_id']  # Hat Team 1 gewonnen?
        t1_color = self.colors['accent_green'] if t1_win else 'white'  # Grün für Gewinner
        t1_weight = 'bold' if t1_win else 'normal'  # Fett für Gewinner

        t1_frame = tk.Frame(center, bg=self.colors['bg_light'])
        t1_frame.pack(fill=tk.X)

        # Team 1 Name (links)
        tk.Label(t1_frame, text=f"{match['team1_name']} ({match['team1_abbr']})",
                font=('Segoe UI', 12, t1_weight),
                bg=self.colors['bg_light'],
                fg=t1_color).pack(side=tk.LEFT)

        # Team 1 Score (rechts)
        tk.Label(t1_frame, text=str(match['score_team1']),
                font=('Segoe UI', 14, 'bold'),
                bg=self.colors['bg_light'],
                fg=t1_color).pack(side=tk.RIGHT)

        # ----- VS TRENNLINIE -----
        tk.Label(center, text="─────────── VS ───────────",
                font=('Segoe UI', 8),
                bg=self.colors['bg_light'],
                fg=self.colors['text_dim']).pack(pady=3)

        # ----- TEAM 2 -----
        t2_win = match['winner_team_id'] == match['team2_id']
        t2_color = self.colors['accent_green'] if t2_win else 'white'
        t2_weight = 'bold' if t2_win else 'normal'

        t2_frame = tk.Frame(center, bg=self.colors['bg_light'])
        t2_frame.pack(fill=tk.X)

        # Team 2 Name (links)
        tk.Label(t2_frame, text=f"{match['team2_name']} ({match['team2_abbr']})",
                font=('Segoe UI', 12, t2_weight),
                bg=self.colors['bg_light'],
                fg=t2_color).pack(side=tk.LEFT)

        # Team 2 Score (rechts)
        tk.Label(t2_frame, text=str(match['score_team2']),
                font=('Segoe UI', 14, 'bold'),
                bg=self.colors['bg_light'],
                fg=t2_color).pack(side=tk.RIGHT)

        # ===== RECHTE SEITE: Gewinner =====
        right = tk.Frame(inner, bg=self.colors['bg_light'], width=100)
        right.pack(side=tk.RIGHT, fill=tk.Y)
        right.pack_propagate(False)

        # Gewinner-Anzeige (nur wenn es einen Gewinner gibt)
        if match['winner_name']:
            # "WINNER" Badge
            tk.Label(right, text="🏆 WINNER",
                    font=('Segoe UI', 8, 'bold'),
                    bg=self.colors['accent_green'],
                    fg='white',
                    padx=8, pady=2).pack(pady=(0, 5))

            # Gewinner-Name
            tk.Label(right, text=match['winner_name'],
                    font=('Segoe UI', 9, 'bold'),
                    bg=self.colors['bg_light'],
                    fg=self.colors['accent_green']).pack()

    def update_table_header(self):
        """
        Aktualisiert den Header basierend auf der aktuellen Tabelle.

        Setzt den Titel mit dem entsprechenden Icon und Namen
        der aktuell ausgewählten Tabelle.
        """
        # Icons für jede Tabelle
        icons = {
            'teams': '🏆',
            'players': '👤',
            'tournaments': '🎯',
            'matches': '⚔️',
            'users': '👥'
        }
        display_name = self.tables[self.current_table]['display_name']
        icon = icons.get(self.current_table, '📋')
        self.header_label.config(text=f"{icon} {display_name}")

    # ==========================================================================
    # DATEN LADEN UND ANZEIGEN
    # ==========================================================================

    def load_data(self, search_term: str = None):
        """
        Lädt Daten in die Tabelle.

        Führt eine SQL-Abfrage aus und füllt die Treeview-Tabelle
        mit den Ergebnissen. Unterstützt optionale Suche.

        Args:
            search_term (str, optional): Suchbegriff zum Filtern der Daten
        """
        # Bei Matches spezielle Ansicht verwenden
        if self.current_table == 'matches':
            self.show_matches_view()
            return

        table_info = self.tables[self.current_table]

        # ===== TREEVIEW KONFIGURIEREN =====
        # Alte Daten löschen
        self.tree.delete(*self.tree.get_children())

        # Spalten setzen
        self.tree['columns'] = table_info['columns']
        self.tree['show'] = 'headings'  # Nur Spaltenüberschriften anzeigen, keine Baumstruktur

        # Spaltenüberschriften und Breiten konfigurieren
        for col, header in zip(table_info['columns'], table_info['headers']):
            self.tree.heading(col, text=header, anchor='w')
            # Breitere Spalten für längere Texte
            width = 150 if col in ['team_name', 'tournament_name', 'email'] else 100
            self.tree.column(col, width=width, anchor='w')

        # ===== DATEN LADEN =====
        # Spieler-Tabelle braucht JOIN für Teamname
        if self.current_table == 'players':
            query = """
                SELECT p.player_id, p.nickname, p.first_name, p.last_name, p.role,
                       COALESCE(t.team_name, 'Kein Team') as team_name
                FROM PLAYERS p
                LEFT JOIN TEAMS t ON p.team_id = t.team_id
            """
            if search_term:
                # Suche in mehreren Spalten
                query += " WHERE p.nickname LIKE %s OR p.first_name LIKE %s OR t.team_name LIKE %s"
                data = self.db.execute(query, tuple([f"%{search_term}%"] * 3))
            else:
                data = self.db.execute(query)
        else:
            # Andere Tabellen: einfache SELECT-Abfrage
            if search_term:
                # Suche in allen Spalten
                conditions = " OR ".join([f"{col} LIKE %s" for col in table_info['columns']])
                query = f"SELECT * FROM {table_info['name']} WHERE {conditions}"
                data = self.db.execute(query, tuple([f"%{search_term}%"] * len(table_info['columns'])))
            else:
                data = self.db.execute(f"SELECT * FROM {table_info['name']}")

        # ===== DATEN IN TREEVIEW EINFÜGEN =====
        if data:
            for row in data:
                # Werte aus dem Dictionary extrahieren und formatieren
                values = [self.format_value(row.get(col)) for col in table_info['columns']]
                self.tree.insert('', tk.END, values=values)

        # Statusleiste aktualisieren
        count = len(data) if data else 0
        self.status_label.config(text=f"{count} Datensätze geladen")

    def format_value(self, value) -> str:
        """
        Formatiert Werte für die Anzeige.

        Konvertiert verschiedene Datentypen in lesbare Strings:
        - None -> leerer String
        - Datum/Zeit -> deutsches Format
        - Dezimalzahlen -> Währungsformat

        Args:
            value: Der zu formatierende Wert

        Returns:
            str: Formatierter String für die Anzeige
        """
        if value is None:
            return ""
        if isinstance(value, datetime):
            return value.strftime("%d.%m.%Y %H:%M")  # z.B. "15.01.2025 14:30"
        if isinstance(value, date):
            return value.strftime("%d.%m.%Y")        # z.B. "15.01.2025"
        if isinstance(value, Decimal):
            return f"${float(value):,.0f}"          # z.B. "$1,000,000"
        return str(value)

    # ==========================================================================
    # SUCHE
    # ==========================================================================

    def on_search(self, *args):
        """
        Handler für Suche.

        Wird automatisch aufgerufen, wenn sich der Text im Suchfeld ändert.
        Lädt die Daten neu mit dem aktuellen Suchbegriff.

        Args:
            *args: Tkinter trace-Argumente (werden ignoriert)
        """
        search_term = self.search_var.get()
        if self.current_table == 'matches':
            self.show_matches_view()  # Match-Ansicht neu laden (TODO: Suche implementieren)
        else:
            # Daten mit Suchbegriff laden (oder ohne, wenn leer)
            self.load_data(search_term if search_term else None)

    def refresh_view(self):
        """
        Aktualisiert die aktuelle Ansicht.

        Lädt die Caches neu und aktualisiert die Anzeige.
        Wird nach Änderungen oder manuell über das Menü aufgerufen.
        """
        self.refresh_caches()
        if self.current_table == 'matches':
            self.show_matches_view()
        else:
            self.load_data()

    # ==========================================================================
    # CRUD OPERATIONEN
    # ==========================================================================

    def add_record(self):
        """
        Öffnet Dialog zum Hinzufügen eines neuen Datensatzes.

        Ruft open_record_dialog im "Hinzufügen"-Modus auf.
        """
        self.open_record_dialog("Hinzufügen")

    def edit_record(self):
        """
        Öffnet Dialog zum Bearbeiten eines ausgewählten Datensatzes.

        Prüft, ob ein Datensatz ausgewählt ist, lädt dessen Daten
        und öffnet den Bearbeiten-Dialog.
        """
        if self.current_table == 'matches':
            # Match-Ansicht: Auswahl über selected_match_id
            if not self.selected_match_id:
                messagebox.showwarning("Hinweis", "Bitte ein Match auswählen (klicken).")
                return
            # Match-Daten laden
            result = self.db.execute("SELECT * FROM MATCHES WHERE match_id = %s", (self.selected_match_id,))
            if result:
                self.open_record_dialog("Bearbeiten", result[0])
        else:
            # Tabellen-Ansicht: Auswahl über Treeview-Selektion
            selection = self.tree.selection()
            if not selection:
                messagebox.showwarning("Hinweis", "Bitte einen Datensatz auswählen.")
                return

            # ID aus der ersten Spalte der ausgewählten Zeile
            record_id = self.tree.item(selection[0])['values'][0]
            table_info = self.tables[self.current_table]

            # Datensatz aus der Datenbank laden
            result = self.db.execute(f"SELECT * FROM {table_info['name']} WHERE {table_info['pk']} = %s", (record_id,))

            if result:
                self.open_record_dialog("Bearbeiten", result[0])

    def delete_record(self):
        """
        Löscht einen ausgewählten Datensatz.

        Zeigt einen Bestätigungsdialog und löscht bei Bestätigung
        den ausgewählten Datensatz aus der Datenbank.
        """
        # ID des zu löschenden Datensatzes ermitteln
        if self.current_table == 'matches':
            if not self.selected_match_id:
                messagebox.showwarning("Hinweis", "Bitte ein Match auswählen.")
                return
            record_id = self.selected_match_id
        else:
            selection = self.tree.selection()
            if not selection:
                messagebox.showwarning("Hinweis", "Bitte einen Datensatz auswählen.")
                return
            record_id = self.tree.item(selection[0])['values'][0]

        table_info = self.tables[self.current_table]

        # Bestätigungsdialog anzeigen
        if messagebox.askyesno("Löschen bestätigen", f"Datensatz {record_id} wirklich löschen?"):
            # DELETE-Abfrage ausführen
            self.db.execute(f"DELETE FROM {table_info['name']} WHERE {table_info['pk']} = %s", (record_id,))
            self.selected_match_id = None  # Auswahl zurücksetzen
            self.refresh_view()            # Ansicht aktualisieren
            self.status_label.config(text=f"Datensatz {record_id} gelöscht")

    def open_record_dialog(self, mode: str, data: Dict = None):
        """
        Öffnet einen Dialog zum Hinzufügen/Bearbeiten eines Datensatzes.

        Erstellt ein dynamisches Formular basierend auf der Tabellenkonfiguration.

        Args:
            mode (str): "Hinzufügen" oder "Bearbeiten"
            data (Dict, optional): Vorhandene Daten zum Bearbeiten
        """
        table_info = self.tables[self.current_table]

        # ===== DIALOG-FENSTER ERSTELLEN =====
        dialog = tk.Toplevel(self.root)
        dialog.title(f"{table_info['display_name']} {mode}")
        dialog.geometry("500x550")
        dialog.resizable(False, False)
        dialog.transient(self.root)  # Über Hauptfenster anzeigen
        dialog.grab_set()            # Modal
        dialog.configure(bg=self.colors['bg_medium'])

        # Dialog zentrieren
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() - 500) // 2
        y = (dialog.winfo_screenheight() - 550) // 2
        dialog.geometry(f"+{x}+{y}")

        # ===== TITEL =====
        tk.Label(dialog, text=f"📝 {table_info['display_name']} {mode}",
                font=('Segoe UI', 14, 'bold'),
                bg=self.colors['bg_medium'],
                fg='white').pack(pady=15)

        # ===== SCROLLBARER FORMULAR-BEREICH =====
        canvas = tk.Canvas(dialog, bg=self.colors['bg_medium'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(dialog, orient="vertical", command=canvas.yview)
        form_frame = tk.Frame(canvas, bg=self.colors['bg_medium'])

        form_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=form_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # ===== FORMULARFELDER ERSTELLEN =====
        entries = {}  # Dictionary zum Speichern der Eingabe-Widgets

        for field_info in table_info['form_fields']:
            field_name = field_info[0]   # DB-Feldname
            label_text = field_info[1]   # Anzeigelabel
            field_type = field_info[2]   # Feldtyp (entry, combo, team_combo, etc.)

            # Label für das Feld
            tk.Label(form_frame, text=label_text,
                    font=('Segoe UI', 10),
                    bg=self.colors['bg_medium'],
                    fg=self.colors['text_dim'],
                    anchor='w').pack(fill=tk.X, pady=(10, 2))

            # ----- DROPDOWN (COMBO) -----
            if field_type == 'combo':
                options = field_info[3]  # Verfügbare Optionen
                var = tk.StringVar()
                combo = ttk.Combobox(form_frame, textvariable=var, values=options,
                                    font=('Segoe UI', 11), state='readonly')
                combo.pack(fill=tk.X, ipady=5)
                entries[field_name] = var

                # Vorhandenen Wert setzen oder erste Option
                if data and field_name in data and data[field_name]:
                    var.set(data[field_name])
                elif options:
                    var.set(options[0])

            # ----- TEAM-DROPDOWN -----
            elif field_type in ['team_combo', 'team_combo_optional']:
                var = tk.StringVar()
                # Optionen aus dem Team-Cache erstellen
                opts = [f"{t['team_id']}: {t['team_name']} ({t['abbreviation']})" for t in self.teams_cache]
                if field_type == 'team_combo_optional':
                    opts = ["-- Kein Gewinner --"] + opts  # Optional: kann leer sein

                combo = ttk.Combobox(form_frame, textvariable=var, values=opts,
                                    font=('Segoe UI', 11), state='readonly')
                combo.pack(fill=tk.X, ipady=5)
                entries[field_name] = var

                # Vorhandenen Wert setzen
                if data and field_name in data and data[field_name]:
                    for opt in opts:
                        if opt.startswith(f"{data[field_name]}:"):
                            var.set(opt)
                            break
                elif field_type == 'team_combo_optional':
                    var.set("-- Kein Gewinner --")

            # ----- TURNIER-DROPDOWN -----
            elif field_type == 'tournament_combo':
                var = tk.StringVar()
                opts = [f"{t['tournament_id']}: {t['tournament_name']}" for t in self.tournaments_cache]

                combo = ttk.Combobox(form_frame, textvariable=var, values=opts,
                                    font=('Segoe UI', 11), state='readonly')
                combo.pack(fill=tk.X, ipady=5)
                entries[field_name] = var

                if data and field_name in data and data[field_name]:
                    for opt in opts:
                        if opt.startswith(f"{data[field_name]}:"):
                            var.set(opt)
                            break

            # ----- TEXT-EINGABEFELD -----
            else:  # field_type == 'entry'
                entry = tk.Entry(form_frame,
                               font=('Segoe UI', 11),
                               bg=self.colors['bg_dark'],
                               fg='white',
                               insertbackground='white',
                               relief=tk.FLAT)
                entry.pack(fill=tk.X, ipady=8)
                entries[field_name] = entry

                # Vorhandenen Wert setzen
                if data and field_name in data and data[field_name] is not None:
                    value = data[field_name]
                    # Datum/Zeit formatieren
                    if isinstance(value, datetime):
                        value = value.strftime("%Y-%m-%d %H:%M")
                    elif isinstance(value, date):
                        value = value.strftime("%Y-%m-%d")
                    entry.insert(0, str(value))

        # ===== SPEICHERN-FUNKTION =====
        def save():
            """Speichert den Datensatz in der Datenbank."""
            values = {}

            # Werte aus allen Eingabefeldern sammeln
            for field_name, widget in entries.items():
                if isinstance(widget, tk.StringVar):
                    value = widget.get()
                    # Bei Combo-Feldern: ID extrahieren (Format: "ID: Name")
                    if value and ':' in value and field_name in ['team_id', 'team1_id', 'team2_id', 'winner_team_id', 'tournament_id']:
                        if value.startswith("--"):
                            value = None  # "-- Kein Gewinner --" -> NULL
                        else:
                            value = value.split(':')[0]  # Nur ID
                else:
                    value = widget.get()

                if value:
                    values[field_name] = value
                elif field_name == 'winner_team_id':
                    values[field_name] = None  # winner_team_id darf NULL sein

            # Validierung: Mindestens ein Feld muss ausgefüllt sein
            if not values:
                messagebox.showwarning("Hinweis", "Bitte mindestens ein Feld ausfüllen.")
                return

            # SQL-Abfrage erstellen und ausführen
            if mode == "Hinzufügen":
                # INSERT-Statement
                columns = ', '.join(values.keys())
                placeholders = ', '.join(['%s'] * len(values))
                query = f"INSERT INTO {table_info['name']} ({columns}) VALUES ({placeholders})"
                self.db.execute(query, tuple(values.values()))
                self.status_label.config(text="Datensatz hinzugefügt")
            else:
                # UPDATE-Statement
                set_clause = ', '.join([f"{k} = %s" for k in values.keys()])
                query = f"UPDATE {table_info['name']} SET {set_clause} WHERE {table_info['pk']} = %s"
                self.db.execute(query, tuple(list(values.values()) + [data[table_info['pk']]]))
                self.status_label.config(text="Datensatz aktualisiert")

            # Dialog schließen und Ansicht aktualisieren
            dialog.destroy()
            self.refresh_caches()
            self.refresh_view()

        # ===== BUTTONS =====
        btn_frame = tk.Frame(dialog, bg=self.colors['bg_medium'])
        btn_frame.pack(fill=tk.X, padx=20, pady=20)

        # Speichern-Button
        tk.Button(btn_frame, text="💾 Speichern",
                 font=('Segoe UI', 11, 'bold'),
                 bg=self.colors['accent'],
                 fg='white',
                 relief=tk.FLAT,
                 padx=25, pady=10,
                 command=save).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 5))

        # Abbrechen-Button
        tk.Button(btn_frame, text="❌ Abbrechen",
                 font=('Segoe UI', 11),
                 bg=self.colors['bg_light'],
                 fg='white',
                 relief=tk.FLAT,
                 padx=25, pady=10,
                 command=dialog.destroy).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(5, 0))

    # ==========================================================================
    # IMPORT/EXPORT FUNKTIONEN
    # ==========================================================================

    def export_json(self):
        """
        Exportiert die aktuelle Tabelle als JSON-Datei.

        Öffnet einen Speichern-Dialog und exportiert alle Daten
        der aktuellen Tabelle im JSON-Format.
        """
        table_info = self.tables[self.current_table]

        # Speichern-Dialog öffnen
        filepath = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON Dateien", "*.json")],
            initialfile=f"{self.current_table}_export.json"  # Vorgeschlagener Dateiname
        )

        if not filepath:
            return  # Abgebrochen

        # Daten aus der Datenbank laden
        data = self.db.execute(f"SELECT * FROM {table_info['name']}")

        if data:
            # Daten für JSON serialisieren (Datum/Decimal konvertieren)
            export_data = []
            for row in data:
                export_data.append({k: self.serialize_value(v) for k, v in row.items()})

            # In Datei schreiben
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, ensure_ascii=False, indent=2)

            messagebox.showinfo("Export erfolgreich", f"✅ {len(data)} Datensätze exportiert!\n\n{filepath}")
            self.status_label.config(text=f"Export: {len(data)} Datensätze nach {filepath}")
        else:
            messagebox.showwarning("Export", "Keine Daten zum Exportieren.")

    def export_csv(self):
        """
        Exportiert die aktuelle Tabelle als CSV-Datei.

        Öffnet einen Speichern-Dialog und exportiert alle Daten
        der aktuellen Tabelle im CSV-Format.
        """
        table_info = self.tables[self.current_table]

        filepath = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV Dateien", "*.csv")],
            initialfile=f"{self.current_table}_export.csv"
        )

        if not filepath:
            return

        data = self.db.execute(f"SELECT * FROM {table_info['name']}")

        if data:
            # CSV-Datei schreiben
            with open(filepath, 'w', encoding='utf-8', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=data[0].keys())
                writer.writeheader()  # Spaltenüberschriften schreiben
                for row in data:
                    writer.writerow({k: self.serialize_value(v) for k, v in row.items()})

            messagebox.showinfo("Export erfolgreich", f"✅ {len(data)} Datensätze exportiert!\n\n{filepath}")
            self.status_label.config(text=f"Export: {len(data)} Datensätze nach {filepath}")
        else:
            messagebox.showwarning("Export", "Keine Daten zum Exportieren.")

    def import_json(self):
        """
        Importiert Daten aus einer JSON-Datei.

        Öffnet einen Datei-Dialog und importiert die JSON-Daten
        in die aktuelle Tabelle.
        """
        filepath = filedialog.askopenfilename(
            filetypes=[("JSON Dateien", "*.json")]
        )

        if not filepath:
            return

        table_info = self.tables[self.current_table]

        try:
            # JSON-Datei lesen
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)

            count = 0
            for row in data:
                # Primary Key entfernen (wird automatisch generiert)
                row.pop(table_info['pk'], None)

                if row:
                    # INSERT-Statement erstellen
                    columns = ', '.join(row.keys())
                    placeholders = ', '.join(['%s'] * len(row))
                    query = f"INSERT INTO {table_info['name']} ({columns}) VALUES ({placeholders})"
                    self.db.execute(query, tuple(row.values()))
                    count += 1

            messagebox.showinfo("Import erfolgreich", f"✅ {count} Datensätze importiert!")
            self.status_label.config(text=f"Import: {count} Datensätze aus {filepath}")
            self.refresh_view()

        except Exception as e:
            messagebox.showerror("Import-Fehler", str(e))

    def import_csv(self):
        """
        Importiert Daten aus einer CSV-Datei.

        Öffnet einen Datei-Dialog und importiert die CSV-Daten
        in die aktuelle Tabelle.
        """
        filepath = filedialog.askopenfilename(
            filetypes=[("CSV Dateien", "*.csv")]
        )

        if not filepath:
            return

        table_info = self.tables[self.current_table]

        try:
            # CSV-Datei lesen
            with open(filepath, 'r', encoding='utf-8') as f:
                data = list(csv.DictReader(f))

            count = 0
            for row in data:
                # Primary Key entfernen
                row.pop(table_info['pk'], None)

                # Leere Werte auf None setzen (für Datenbank)
                cleaned = {k: (v if v else None) for k, v in row.items()}

                if any(cleaned.values()):  # Mindestens ein Wert vorhanden
                    columns = ', '.join(cleaned.keys())
                    placeholders = ', '.join(['%s'] * len(cleaned))
                    query = f"INSERT INTO {table_info['name']} ({columns}) VALUES ({placeholders})"
                    self.db.execute(query, tuple(cleaned.values()))
                    count += 1

            messagebox.showinfo("Import erfolgreich", f"✅ {count} Datensätze importiert!")
            self.status_label.config(text=f"Import: {count} Datensätze aus {filepath}")
            self.refresh_view()

        except Exception as e:
            messagebox.showerror("Import-Fehler", str(e))

    def serialize_value(self, value) -> Any:
        """
        Serialisiert Werte für JSON/CSV Export.

        Konvertiert Python-Objekte in JSON-kompatible Typen:
        - datetime/date -> ISO-Format String
        - Decimal -> float

        Args:
            value: Der zu serialisierende Wert

        Returns:
            Any: JSON-kompatibler Wert
        """
        if isinstance(value, (datetime, date)):
            return value.isoformat()  # z.B. "2025-01-15" oder "2025-01-15T14:30:00"
        if isinstance(value, Decimal):
            return float(value)       # Decimal -> float
        return value

    # ==========================================================================
    # STATISTIKEN UND INFO
    # ==========================================================================

    def show_statistics(self):
        """
        Zeigt Statistik-Dialog mit Datensatz-Anzahl pro Tabelle.

        Öffnet ein modales Fenster mit einer Übersicht über
        die Anzahl der Datensätze in jeder Tabelle.
        """
        # Dialog erstellen
        dialog = tk.Toplevel(self.root)
        dialog.title("📊 Statistiken")
        dialog.geometry("400x350")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.configure(bg=self.colors['bg_medium'])

        # Zentrieren
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() - 400) // 2
        y = (dialog.winfo_screenheight() - 350) // 2
        dialog.geometry(f"+{x}+{y}")

        # Titel
        tk.Label(dialog, text="📊 Datenbank-Statistiken",
                font=('Segoe UI', 16, 'bold'),
                bg=self.colors['bg_medium'],
                fg='white').pack(pady=20)

        # Container für Statistik-Zeilen
        stats_frame = tk.Frame(dialog, bg=self.colors['bg_medium'])
        stats_frame.pack(fill=tk.BOTH, expand=True, padx=30)

        # Icons für jede Tabelle
        icons = {'teams': '🏆', 'players': '👤', 'tournaments': '🎯', 'matches': '⚔️', 'users': '👥'}

        # Für jede Tabelle eine Zeile erstellen
        for table_key, table_info in self.tables.items():
            # Anzahl der Datensätze abfragen
            result = self.db.execute(f"SELECT COUNT(*) as count FROM {table_info['name']}")
            count = result[0]['count'] if result else 0

            # Zeile erstellen
            row = tk.Frame(stats_frame, bg=self.colors['bg_dark'])
            row.pack(fill=tk.X, pady=5, ipady=10)

            # Icon und Tabellenname (links)
            tk.Label(row, text=f"  {icons.get(table_key, '📋')}  {table_info['display_name']}",
                    font=('Segoe UI', 12),
                    bg=self.colors['bg_dark'],
                    fg='white').pack(side=tk.LEFT, padx=10)

            # Anzahl (rechts, hervorgehoben)
            tk.Label(row, text=str(count),
                    font=('Segoe UI', 14, 'bold'),
                    bg=self.colors['bg_dark'],
                    fg=self.colors['accent']).pack(side=tk.RIGHT, padx=20)

        # Schließen-Button
        tk.Button(dialog, text="Schließen",
                 font=('Segoe UI', 10),
                 bg=self.colors['bg_light'],
                 fg='white',
                 relief=tk.FLAT,
                 padx=30, pady=8,
                 command=dialog.destroy).pack(pady=20)

    def show_about(self):
        """
        Zeigt Über-Dialog mit Programminformationen.

        Zeigt Version, Autor und Features des Programms.
        """
        messagebox.showinfo("Über",
                          "🎮 CS2 E-Sport Management System\n\n"
                          "Version: 1.1\n"
                          "Autor: Joel\n"
                          "Projekt: BTS Datenbankprojekt 2025\n\n"
                          "Features:\n"
                          "- CRUD-Operationen\n"
                          "- Import/Export (JSON/CSV)\n"
                          "- Match-Karten-Ansicht\n"
                          "- Live-Suche")

    # ==========================================================================
    # PROGRAMMENDE
    # ==========================================================================

    def on_closing(self):
        """
        Handler beim Schließen der Anwendung.

        Trennt die Datenbankverbindung sauber und schließt das Fenster.
        Wird aufgerufen, wenn der Benutzer das Fenster schließt.
        """
        self.db.disconnect()  # Datenbankverbindung trennen
        self.root.destroy()   # Fenster schließen


# ==============================================================================
# PROGRAMM-EINSTIEGSPUNKT
# ==============================================================================

def main():
    """
    Haupteinstiegspunkt der Anwendung.

    Erstellt das Tkinter-Hauptfenster, initialisiert die Anwendung
    und startet die Event-Loop.
    """
    root = tk.Tk()              # Hauptfenster erstellen
    app = CS2EsportApp(root)    # Anwendung initialisieren
    root.mainloop()             # Event-Loop starten (wartet auf Benutzerinteraktion)


# Programm nur ausführen, wenn direkt gestartet (nicht importiert)
if __name__ == "__main__":
    main()

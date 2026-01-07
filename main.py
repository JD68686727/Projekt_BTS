#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
==============================================================================
CS2 E-SPORT MANAGEMENT SYSTEM - Hauptprogramm
==============================================================================
Projekt:     CS2 E-Sport Organisation Management
Autor:       Joel - BTS Datenbankprojekt
Datum:       Januar 2025
Datenbank:   MariaDB / MySQL
Python:      3.10+

Beschreibung:
    Dieses Programm ermöglicht die Verwaltung einer CS2 E-Sport Organisation.
    Es bietet vollständige CRUD-Operationen (Create, Read, Update, Delete),
    Suchfunktionen sowie Import/Export von Daten im JSON- und CSV-Format.

Tabellen: USERS, TEAMS, PLAYERS, TOURNAMENTS, MATCHES
==============================================================================
"""

import os, sys, json, csv
from datetime import datetime
from decimal import Decimal
from typing import Optional, List, Dict, Any

try:
    import mysql.connector
    from mysql.connector import Error as MySQLError
except ImportError:
    print("FEHLER: pip install mysql-connector-python")
    sys.exit(1)

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None

# ==============================================================================
# KONFIGURATION
# ==============================================================================
class Config:
    """Konfigurationsklasse - lädt aus .env oder verwendet Standardwerte."""
    def __init__(self):
        if load_dotenv: load_dotenv()
        self.DB_HOST = os.getenv('DB_HOST', 'localhost')
        self.DB_PORT = int(os.getenv('DB_PORT', '3306'))
        self.DB_USER = os.getenv('DB_USER', 'root')
        self.DB_PASSWORD = os.getenv('DB_PASSWORD', '')
        self.DB_NAME = os.getenv('DB_NAME', 'cs2_esport_db')
        self.EXPORT_PATH = os.getenv('EXPORT_PATH', 'data/export')
        self.IMPORT_PATH = os.getenv('IMPORT_PATH', 'data/import')

# ==============================================================================
# DATENBANKVERBINDUNG
# ==============================================================================
class Database:
    """Datenbankklasse für MariaDB/MySQL Verbindung."""
    def __init__(self, config: Config):
        self.config = config
        self.connection = None
        self.cursor = None
    
    def connect(self) -> bool:
        try:
            self.connection = mysql.connector.connect(
                host=self.config.DB_HOST, port=self.config.DB_PORT,
                user=self.config.DB_USER, password=self.config.DB_PASSWORD,
                database=self.config.DB_NAME, charset='utf8mb4',
                collation='utf8mb4_unicode_ci', autocommit=False
            )
            self.cursor = self.connection.cursor(dictionary=True)
            print(f"✅ Verbunden mit {self.config.DB_NAME}")
            return True
        except MySQLError as e:
            print(f"❌ Datenbankfehler: {e}")
            return False
    
    def disconnect(self):
        if self.cursor: self.cursor.close()
        if self.connection: self.connection.close()
        print("🔌 Verbindung geschlossen.")
    
    def execute(self, query: str, params: tuple = None) -> bool:
        try:
            self.cursor.execute(query, params or ())
            self.connection.commit()
            return True
        except MySQLError as e:
            self.connection.rollback()
            print(f"❌ SQL-Fehler: {e}")
            return False
    
    def fetch_all(self, query: str, params: tuple = None) -> List[Dict]:
        try:
            self.cursor.execute(query, params or ())
            return self.cursor.fetchall()
        except MySQLError as e:
            print(f"❌ Fehler: {e}")
            return []
    
    def fetch_one(self, query: str, params: tuple = None) -> Optional[Dict]:
        try:
            self.cursor.execute(query, params or ())
            return self.cursor.fetchone()
        except MySQLError as e:
            print(f"❌ Fehler: {e}")
            return None
    
    def get_last_insert_id(self) -> int:
        return self.cursor.lastrowid

# ==============================================================================
# CRUD-OPERATIONEN
# ==============================================================================
class CRUDOperations:
    """CRUD für alle Tabellen: Users, Teams, Players, Tournaments, Matches"""
    def __init__(self, db: Database):
        self.db = db
    
    # --- USERS ---
    def create_user(self, username, password_hash, role, email):
        q = "INSERT INTO USERS (username, password_hash, role, email) VALUES (%s,%s,%s,%s)"
        return self.db.get_last_insert_id() if self.db.execute(q, (username, password_hash, role, email)) else None
    
    def get_all_users(self): return self.db.fetch_all("SELECT * FROM USERS ORDER BY user_id")
    def get_user_by_id(self, id): return self.db.fetch_one("SELECT * FROM USERS WHERE user_id=%s", (id,))
    
    def update_user(self, user_id, **kw):
        allowed = {'username','email','role','password_hash','last_login'}
        updates = {k:v for k,v in kw.items() if k in allowed}
        if not updates: return False
        q = f"UPDATE USERS SET {', '.join(f'{k}=%s' for k in updates)} WHERE user_id=%s"
        return self.db.execute(q, tuple(updates.values()) + (user_id,))
    
    def delete_user(self, id): return self.db.execute("DELETE FROM USERS WHERE user_id=%s", (id,))
    
    # --- TEAMS ---
    def create_team(self, team_name, abbreviation=None, country=None, coach=None, founded_date=None):
        q = "INSERT INTO TEAMS (team_name,abbreviation,country,coach,founded_date) VALUES (%s,%s,%s,%s,%s)"
        return self.db.get_last_insert_id() if self.db.execute(q, (team_name,abbreviation,country,coach,founded_date)) else None
    
    def get_all_teams(self): return self.db.fetch_all("SELECT * FROM TEAMS WHERE is_active=TRUE ORDER BY team_name")
    def get_team_by_id(self, id): return self.db.fetch_one("SELECT * FROM TEAMS WHERE team_id=%s", (id,))
    
    def update_team(self, team_id, **kw):
        allowed = {'team_name','abbreviation','country','coach','founded_date','is_active'}
        updates = {k:v for k,v in kw.items() if k in allowed}
        if not updates: return False
        q = f"UPDATE TEAMS SET {', '.join(f'{k}=%s' for k in updates)} WHERE team_id=%s"
        return self.db.execute(q, tuple(updates.values()) + (team_id,))
    
    def delete_team(self, id):
        players = self.db.fetch_all("SELECT player_id FROM PLAYERS WHERE team_id=%s", (id,))
        if players:
            print(f"⚠️ Team hat {len(players)} Spieler. Setze auf inaktiv.")
            return self.db.execute("UPDATE TEAMS SET is_active=FALSE WHERE team_id=%s", (id,))
        return self.db.execute("DELETE FROM TEAMS WHERE team_id=%s", (id,))
    
    # --- PLAYERS ---
    def create_player(self, nickname, team_id=None, real_name=None, nationality=None, role=None, birth_date=None):
        q = "INSERT INTO PLAYERS (nickname,team_id,real_name,nationality,role,birth_date) VALUES (%s,%s,%s,%s,%s,%s)"
        return self.db.get_last_insert_id() if self.db.execute(q, (nickname,team_id,real_name,nationality,role,birth_date)) else None
    
    def get_all_players(self):
        return self.db.fetch_all("""SELECT p.*, t.team_name, t.abbreviation as team_abbr 
            FROM PLAYERS p LEFT JOIN TEAMS t ON p.team_id=t.team_id WHERE p.is_active=TRUE ORDER BY p.nickname""")
    
    def get_player_by_id(self, id):
        return self.db.fetch_one("SELECT p.*, t.team_name FROM PLAYERS p LEFT JOIN TEAMS t ON p.team_id=t.team_id WHERE p.player_id=%s", (id,))
    
    def get_players_by_team(self, team_id):
        return self.db.fetch_all("SELECT * FROM PLAYERS WHERE team_id=%s AND is_active=TRUE ORDER BY role,nickname", (team_id,))
    
    def update_player(self, player_id, **kw):
        allowed = {'nickname','team_id','real_name','nationality','role','birth_date','is_active'}
        updates = {k:v for k,v in kw.items() if k in allowed}
        if not updates: return False
        q = f"UPDATE PLAYERS SET {', '.join(f'{k}=%s' for k in updates)} WHERE player_id=%s"
        return self.db.execute(q, tuple(updates.values()) + (player_id,))
    
    def delete_player(self, id): return self.db.execute("UPDATE PLAYERS SET is_active=FALSE WHERE player_id=%s", (id,))
    
    # --- TOURNAMENTS ---
    def create_tournament(self, tournament_name, start_date, end_date, location=None, prize_pool=None, tier='B-Tier', status='Upcoming'):
        q = "INSERT INTO TOURNAMENTS (tournament_name,location,start_date,end_date,prize_pool,tier,status) VALUES (%s,%s,%s,%s,%s,%s,%s)"
        return self.db.get_last_insert_id() if self.db.execute(q, (tournament_name,location,start_date,end_date,prize_pool,tier,status)) else None
    
    def get_all_tournaments(self): return self.db.fetch_all("SELECT * FROM TOURNAMENTS ORDER BY start_date DESC")
    def get_tournament_by_id(self, id): return self.db.fetch_one("SELECT * FROM TOURNAMENTS WHERE tournament_id=%s", (id,))
    def get_upcoming_tournaments(self): return self.db.fetch_all("SELECT * FROM TOURNAMENTS WHERE status='Upcoming' ORDER BY start_date")
    
    def update_tournament(self, tournament_id, **kw):
        allowed = {'tournament_name','location','start_date','end_date','prize_pool','tier','status'}
        updates = {k:v for k,v in kw.items() if k in allowed}
        if not updates: return False
        q = f"UPDATE TOURNAMENTS SET {', '.join(f'{k}=%s' for k in updates)} WHERE tournament_id=%s"
        return self.db.execute(q, tuple(updates.values()) + (tournament_id,))
    
    def delete_tournament(self, id): return self.db.execute("DELETE FROM TOURNAMENTS WHERE tournament_id=%s", (id,))
    
    # --- MATCHES ---
    def create_match(self, tournament_id, team1_id, team2_id, match_date, best_of='BO3', stage=None):
        if team1_id == team2_id:
            print("❌ Ein Team kann nicht gegen sich selbst spielen!")
            return None
        q = "INSERT INTO MATCHES (tournament_id,team1_id,team2_id,match_date,best_of,stage) VALUES (%s,%s,%s,%s,%s,%s)"
        return self.db.get_last_insert_id() if self.db.execute(q, (tournament_id,team1_id,team2_id,match_date,best_of,stage)) else None
    
    def get_all_matches(self):
        return self.db.fetch_all("""SELECT m.*, t.tournament_name, t1.team_name as team1_name, t1.abbreviation as team1_abbr,
            t2.team_name as team2_name, t2.abbreviation as team2_abbr, tw.team_name as winner_name
            FROM MATCHES m JOIN TOURNAMENTS t ON m.tournament_id=t.tournament_id
            JOIN TEAMS t1 ON m.team1_id=t1.team_id JOIN TEAMS t2 ON m.team2_id=t2.team_id
            LEFT JOIN TEAMS tw ON m.winner_team_id=tw.team_id ORDER BY m.match_date DESC""")
    
    def get_match_by_id(self, id):
        return self.db.fetch_one("""SELECT m.*, t.tournament_name, t1.team_name as team1_name, t2.team_name as team2_name
            FROM MATCHES m JOIN TOURNAMENTS t ON m.tournament_id=t.tournament_id
            JOIN TEAMS t1 ON m.team1_id=t1.team_id JOIN TEAMS t2 ON m.team2_id=t2.team_id WHERE m.match_id=%s""", (id,))
    
    def update_match_score(self, match_id, score1, score2, winner_id=None):
        return self.db.execute("UPDATE MATCHES SET score_team1=%s, score_team2=%s, winner_team_id=%s WHERE match_id=%s",
                               (score1, score2, winner_id, match_id))
    
    def delete_match(self, id): return self.db.execute("DELETE FROM MATCHES WHERE match_id=%s", (id,))

# ==============================================================================
# SUCHFUNKTIONEN
# ==============================================================================
class SearchOperations:
    """Suchoperationen für alle Tabellen."""
    def __init__(self, db: Database):
        self.db = db
    
    def search_players(self, term):
        like = f"%{term}%"
        return self.db.fetch_all("""SELECT p.*, t.team_name FROM PLAYERS p LEFT JOIN TEAMS t ON p.team_id=t.team_id
            WHERE p.nickname LIKE %s OR p.real_name LIKE %s OR p.nationality LIKE %s ORDER BY p.nickname""", (like,like,like))
    
    def search_teams(self, term):
        like = f"%{term}%"
        return self.db.fetch_all("SELECT * FROM TEAMS WHERE team_name LIKE %s OR abbreviation LIKE %s OR country LIKE %s ORDER BY team_name", (like,like,like))
    
    def search_tournaments(self, term=None, tier=None, status=None):
        conds, params = [], []
        if term: conds.append("(tournament_name LIKE %s OR location LIKE %s)"); params.extend([f"%{term}%"]*2)
        if tier: conds.append("tier=%s"); params.append(tier)
        if status: conds.append("status=%s"); params.append(status)
        where = " AND ".join(conds) if conds else "1=1"
        return self.db.fetch_all(f"SELECT * FROM TOURNAMENTS WHERE {where} ORDER BY start_date DESC", tuple(params))
    
    def search_matches_by_team(self, team_id):
        return self.db.fetch_all("""SELECT m.*, t.tournament_name, t1.team_name as team1_name, t2.team_name as team2_name
            FROM MATCHES m JOIN TOURNAMENTS t ON m.tournament_id=t.tournament_id
            JOIN TEAMS t1 ON m.team1_id=t1.team_id JOIN TEAMS t2 ON m.team2_id=t2.team_id
            WHERE m.team1_id=%s OR m.team2_id=%s ORDER BY m.match_date DESC""", (team_id,team_id))
    
    def get_team_statistics(self, team_id):
        team = self.db.fetch_one("SELECT * FROM TEAMS WHERE team_id=%s", (team_id,))
        if not team: return {}
        pc = self.db.fetch_one("SELECT COUNT(*) as c FROM PLAYERS WHERE team_id=%s AND is_active=TRUE", (team_id,))
        wins = self.db.fetch_one("SELECT COUNT(*) as c FROM MATCHES WHERE winner_team_id=%s", (team_id,))
        total = self.db.fetch_one("SELECT COUNT(*) as c FROM MATCHES WHERE team1_id=%s OR team2_id=%s", (team_id,team_id))
        return {'team': team, 'player_count': pc['c'] if pc else 0, 'total_wins': wins['c'] if wins else 0, 'total_matches': total['c'] if total else 0}

# ==============================================================================
# EXPORT / IMPORT
# ==============================================================================
class DataExporter:
    """Export nach JSON und CSV."""
    def __init__(self, db: Database, path: str):
        self.db = db
        self.path = path
        os.makedirs(path, exist_ok=True)
    
    def _serialize(self, v):
        if isinstance(v, datetime): return v.isoformat()
        if isinstance(v, Decimal): return float(v)
        if isinstance(v, bytes): return v.decode('utf-8')
        return v
    
    def export_to_json(self, table, data):
        data = [{k: self._serialize(v) for k,v in row.items()} for row in data]
        fn = f"{table}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        fp = os.path.join(self.path, fn)
        with open(fp, 'w', encoding='utf-8') as f: json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"✅ Exportiert: {fp} ({len(data)} Datensätze)")
        return fp
    
    def export_to_csv(self, table, data):
        if not data: print("⚠️ Keine Daten!"); return ""
        fn = f"{table}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        fp = os.path.join(self.path, fn)
        with open(fp, 'w', newline='', encoding='utf-8') as f:
            w = csv.DictWriter(f, fieldnames=data[0].keys())
            w.writeheader()
            for row in data: w.writerow({k: self._serialize(v) for k,v in row.items()})
        print(f"✅ Exportiert: {fp} ({len(data)} Datensätze)")
        return fp
    
    def export_table(self, table, fmt='json'):
        valid = ['USERS','TEAMS','PLAYERS','TOURNAMENTS','MATCHES']
        if table.upper() not in valid: print(f"❌ Ungültig: {table}"); return ""
        data = self.db.fetch_all(f"SELECT * FROM {table.upper()}")
        return self.export_to_json(table.lower(), data) if fmt=='json' else self.export_to_csv(table.lower(), data)

class DataImporter:
    """Import aus JSON und CSV."""
    def __init__(self, db: Database, path: str):
        self.db = db
        self.path = path
    
    def import_from_json(self, filepath, table):
        try:
            with open(filepath, 'r', encoding='utf-8') as f: data = json.load(f)
            return self._import(data, table)
        except Exception as e: print(f"❌ Fehler: {e}"); return 0
    
    def import_from_csv(self, filepath, table):
        try:
            with open(filepath, 'r', encoding='utf-8') as f: data = list(csv.DictReader(f))
            return self._import(data, table)
        except Exception as e: print(f"❌ Fehler: {e}"); return 0
    
    def _import(self, data, table):
        if not data: return 0
        cols = {
            'USERS': ['username','password_hash','role','email'],
            'TEAMS': ['team_name','abbreviation','country','coach','founded_date','is_active'],
            'PLAYERS': ['team_id','nickname','real_name','nationality','role','birth_date','is_active'],
            'TOURNAMENTS': ['tournament_name','location','start_date','end_date','prize_pool','tier','status'],
            'MATCHES': ['tournament_id','team1_id','team2_id','score_team1','score_team2','match_date','best_of','stage','winner_team_id']
        }
        t = table.upper()
        if t not in cols: print(f"❌ Ungültig: {table}"); return 0
        imported = 0
        for row in data:
            vals, vcols = [], []
            for c in cols[t]:
                if c in row:
                    v = row[c]
                    vals.append(None if v in ('','None') else v)
                    vcols.append(c)
            if vcols:
                q = f"INSERT INTO {t} ({','.join(vcols)}) VALUES ({','.join(['%s']*len(vcols))})"
                try:
                    if self.db.execute(q, tuple(vals)): imported += 1
                except: pass
        print(f"✅ {imported}/{len(data)} importiert.")
        return imported

# ==============================================================================
# CLI - BENUTZEROBERFLÄCHE
# ==============================================================================
class CLI:
    """Command Line Interface."""
    def __init__(self):
        self.config = Config()
        self.db = Database(self.config)
        self.crud = self.search = self.exporter = self.importer = None
    
    def clear(self): os.system('cls' if os.name=='nt' else 'clear')
    def header(self, t): print("\n" + "="*60 + f"\n  {t}\n" + "="*60 + "\n")
    
    def menu(self, title, opts):
        self.header(title)
        for i,o in enumerate(opts,1): print(f"  [{i}] {o}")
        print(f"\n  [0] Zurück/Beenden\n" + "-"*60)
    
    def inp(self, prompt, req=True):
        while True:
            v = input(f"  {prompt}: ").strip()
            if v or not req: return v
            print("  ⚠️ Eingabe erforderlich!")
    
    def choice(self, mx):
        while True:
            try:
                c = int(input("\n  Wahl: "))
                if 0 <= c <= mx: return c
            except: pass
            print(f"  ⚠️ Bitte 0-{mx}!")
    
    def table(self, data, cols=None):
        if not data: print("  Keine Daten."); return
        cols = cols or list(data[0].keys())
        ws = {c: max(len(str(c)), max(len(str(r.get(c,''))) for r in data)) for c in cols}
        h = " | ".join(str(c).ljust(min(ws[c],25)) for c in cols)
        print(f"\n  {h}\n  " + "-"*len(h))
        for r in data[:20]: print("  " + " | ".join(str(r.get(c,'')).ljust(min(ws[c],25))[:25] for c in cols))
        if len(data)>20: print(f"\n  ... +{len(data)-20} weitere")
    
    def run(self):
        self.clear()
        print("\n" + "="*60 + "\n  🎮 CS2 E-SPORT MANAGEMENT SYSTEM\n  BTS Datenbankprojekt - Januar 2025\n" + "="*60)
        
        if not self.db.connect():
            print("\n  ❌ Keine Datenbankverbindung! Prüfe .env Datei.")
            return
        
        self.crud = CRUDOperations(self.db)
        self.search = SearchOperations(self.db)
        self.exporter = DataExporter(self.db, self.config.EXPORT_PATH)
        self.importer = DataImporter(self.db, self.config.IMPORT_PATH)
        
        try:
            while True:
                self.menu("CS2 E-SPORT MANAGEMENT", ["Teams","Spieler","Turniere","Matches","Benutzer","Suchen","Export (JSON/CSV)","Import (JSON/CSV)","Statistiken"])
                c = self.choice(9)
                if c==0: print("\n  👋 Auf Wiedersehen!\n"); break
                [None, self.m_teams, self.m_players, self.m_tournaments, self.m_matches, self.m_users, self.m_search, self.m_export, self.m_import, self.m_stats][c]()
        finally: self.db.disconnect()
    
    # === TEAMS ===
    def m_teams(self):
        while True:
            self.menu("TEAMS", ["Alle anzeigen","Hinzufügen","Bearbeiten","Löschen","Spieler anzeigen"])
            c = self.choice(5)
            if c==0: return
            if c==1: self.table(self.crud.get_all_teams(), ['team_id','team_name','abbreviation','country','coach']); input("\n  [Enter]...")
            elif c==2:
                self.header("TEAM HINZUFÜGEN")
                tid = self.crud.create_team(self.inp("Name"), self.inp("Kürzel",0) or None, self.inp("Land",0) or None, self.inp("Coach",0) or None, self.inp("Gründung YYYY-MM-DD",0) or None)
                if tid: print(f"\n  ✅ Team erstellt (ID {tid})")
                input("\n  [Enter]...")
            elif c==3:
                self.table(self.crud.get_all_teams(), ['team_id','team_name'])
                tid = int(self.inp("Team-ID"))
                t = self.crud.get_team_by_id(tid)
                if t:
                    print(f"\n  Bearbeite: {t['team_name']}")
                    upd = {}
                    n = self.inp(f"Name [{t['team_name']}]",0); upd['team_name'] = n if n else None
                    c = self.inp(f"Coach [{t['coach']}]",0); upd['coach'] = c if c else None
                    upd = {k:v for k,v in upd.items() if v}
                    if upd and self.crud.update_team(tid, **upd): print("  ✅ Aktualisiert!")
                input("\n  [Enter]...")
            elif c==4:
                self.table(self.crud.get_all_teams(), ['team_id','team_name'])
                tid = int(self.inp("Team-ID zum Löschen"))
                if self.inp("Wirklich? (ja/nein)").lower()=='ja' and self.crud.delete_team(tid): print("  ✅ Gelöscht!")
                input("\n  [Enter]...")
            elif c==5:
                self.table(self.crud.get_all_teams(), ['team_id','team_name'])
                self.table(self.crud.get_players_by_team(int(self.inp("Team-ID"))), ['player_id','nickname','role','nationality'])
                input("\n  [Enter]...")
    
    # === PLAYERS ===
    def m_players(self):
        while True:
            self.menu("SPIELER", ["Alle anzeigen","Hinzufügen","Bearbeiten","Löschen"])
            c = self.choice(4)
            if c==0: return
            if c==1: self.table(self.crud.get_all_players(), ['player_id','nickname','team_name','role','nationality']); input("\n  [Enter]...")
            elif c==2:
                self.header("SPIELER HINZUFÜGEN")
                for t in self.crud.get_all_teams(): print(f"    [{t['team_id']}] {t['team_name']}")
                print("\n  Rollen: IGL, AWPer, Entry Fragger, Support, Lurker")
                pid = self.crud.create_player(
                    self.inp("Nickname"), int(self.inp("Team-ID",0) or 0) or None,
                    self.inp("Echter Name",0) or None, self.inp("Nationalität",0) or None,
                    self.inp("Rolle",0) or None, self.inp("Geburtsdatum YYYY-MM-DD",0) or None)
                if pid: print(f"\n  ✅ Spieler erstellt (ID {pid})")
                input("\n  [Enter]...")
            elif c==3:
                self.table(self.crud.get_all_players(), ['player_id','nickname','team_name'])
                pid = int(self.inp("Spieler-ID"))
                p = self.crud.get_player_by_id(pid)
                if p:
                    upd = {}
                    t = self.inp(f"Team-ID [{p['team_id']}]",0); upd['team_id'] = int(t) if t else None
                    r = self.inp(f"Rolle [{p['role']}]",0); upd['role'] = r if r else None
                    upd = {k:v for k,v in upd.items() if v is not None}
                    if upd and self.crud.update_player(pid, **upd): print("  ✅ Aktualisiert!")
                input("\n  [Enter]...")
            elif c==4:
                self.table(self.crud.get_all_players(), ['player_id','nickname'])
                if self.crud.delete_player(int(self.inp("Spieler-ID"))): print("  ✅ Deaktiviert!")
                input("\n  [Enter]...")
    
    # === TOURNAMENTS ===
    def m_tournaments(self):
        while True:
            self.menu("TURNIERE", ["Alle anzeigen","Kommende","Hinzufügen","Bearbeiten","Löschen"])
            c = self.choice(5)
            if c==0: return
            if c==1: self.table(self.crud.get_all_tournaments(), ['tournament_id','tournament_name','tier','start_date','prize_pool','status']); input("\n  [Enter]...")
            elif c==2: self.table(self.crud.get_upcoming_tournaments(), ['tournament_id','tournament_name','location','start_date','tier']); input("\n  [Enter]...")
            elif c==3:
                self.header("TURNIER HINZUFÜGEN")
                print("  Tiers: S-Tier, A-Tier, B-Tier, C-Tier")
                tid = self.crud.create_tournament(
                    self.inp("Name"), self.inp("Start YYYY-MM-DD"), self.inp("Ende YYYY-MM-DD"),
                    self.inp("Ort",0) or None, float(self.inp("Preisgeld",0) or 0) or None,
                    self.inp("Tier",0) or 'B-Tier')
                if tid: print(f"\n  ✅ Turnier erstellt (ID {tid})")
                input("\n  [Enter]...")
            elif c==4:
                self.table(self.crud.get_all_tournaments(), ['tournament_id','tournament_name','status'])
                tid = int(self.inp("Turnier-ID"))
                t = self.crud.get_tournament_by_id(tid)
                if t:
                    print("  Status: Upcoming, Ongoing, Completed, Cancelled")
                    upd = {}
                    s = self.inp(f"Status [{t['status']}]",0); upd['status'] = s if s else None
                    p = self.inp(f"Preisgeld [{t['prize_pool']}]",0); upd['prize_pool'] = float(p) if p else None
                    upd = {k:v for k,v in upd.items() if v}
                    if upd and self.crud.update_tournament(tid, **upd): print("  ✅ Aktualisiert!")
                input("\n  [Enter]...")
            elif c==5:
                self.table(self.crud.get_all_tournaments(), ['tournament_id','tournament_name'])
                tid = int(self.inp("Turnier-ID"))
                if self.inp("Löscht auch alle Matches! Sicher? (ja/nein)").lower()=='ja' and self.crud.delete_tournament(tid): print("  ✅ Gelöscht!")
                input("\n  [Enter]...")
    
    # === MATCHES ===
    def m_matches(self):
        while True:
            self.menu("MATCHES", ["Alle anzeigen","Hinzufügen","Ergebnis eintragen","Löschen"])
            c = self.choice(4)
            if c==0: return
            if c==1: self.table(self.crud.get_all_matches(), ['match_id','tournament_name','team1_abbr','score_team1','score_team2','team2_abbr','stage']); input("\n  [Enter]...")
            elif c==2:
                self.header("MATCH HINZUFÜGEN")
                for t in self.crud.get_all_tournaments()[:10]: print(f"    [{t['tournament_id']}] {t['tournament_name']}")
                tour = int(self.inp("\nTurnier-ID"))
                for t in self.crud.get_all_teams(): print(f"    [{t['team_id']}] {t['team_name']}")
                t1,t2 = int(self.inp("\nTeam 1 ID")), int(self.inp("Team 2 ID"))
                print("\n  Formate: BO1, BO3, BO5")
                mid = self.crud.create_match(tour, t1, t2, self.inp("Datum YYYY-MM-DD HH:MM:SS"), self.inp("Format",0) or 'BO3', self.inp("Phase",0) or None)
                if mid: print(f"\n  ✅ Match erstellt (ID {mid})")
                input("\n  [Enter]...")
            elif c==3:
                self.table(self.crud.get_all_matches(), ['match_id','team1_name','team2_name'])
                mid = int(self.inp("Match-ID"))
                m = self.crud.get_match_by_id(mid)
                if m:
                    print(f"\n  {m['team1_name']} vs {m['team2_name']}")
                    s1,s2 = int(self.inp(f"Score {m['team1_name']}")), int(self.inp(f"Score {m['team2_name']}"))
                    w = m['team1_id'] if s1>s2 else (m['team2_id'] if s2>s1 else None)
                    if self.crud.update_match_score(mid, s1, s2, w): print("  ✅ Ergebnis eingetragen!")
                input("\n  [Enter]...")
            elif c==4:
                self.table(self.crud.get_all_matches(), ['match_id','team1_name','team2_name'])
                if self.crud.delete_match(int(self.inp("Match-ID"))): print("  ✅ Gelöscht!")
                input("\n  [Enter]...")
    
    # === USERS ===
    def m_users(self):
        while True:
            self.menu("BENUTZER", ["Alle anzeigen","Hinzufügen","Bearbeiten","Löschen"])
            c = self.choice(4)
            if c==0: return
            if c==1: self.table(self.crud.get_all_users(), ['user_id','username','email','role','created_at']); input("\n  [Enter]...")
            elif c==2:
                self.header("BENUTZER HINZUFÜGEN")
                print("  Rollen: Admin, Manager, Viewer")
                uid = self.crud.create_user(self.inp("Username"), f"hashed_{self.inp('Passwort')}", self.inp("Rolle",0) or 'Viewer', self.inp("E-Mail"))
                if uid: print(f"\n  ✅ Benutzer erstellt (ID {uid})")
                input("\n  [Enter]...")
            elif c==3:
                self.table(self.crud.get_all_users(), ['user_id','username','role'])
                uid = int(self.inp("User-ID"))
                u = self.crud.get_user_by_id(uid)
                if u:
                    upd = {}
                    r = self.inp(f"Rolle [{u['role']}]",0); upd['role'] = r if r else None
                    e = self.inp(f"E-Mail [{u['email']}]",0); upd['email'] = e if e else None
                    upd = {k:v for k,v in upd.items() if v}
                    if upd and self.crud.update_user(uid, **upd): print("  ✅ Aktualisiert!")
                input("\n  [Enter]...")
            elif c==4:
                self.table(self.crud.get_all_users(), ['user_id','username'])
                uid = int(self.inp("User-ID"))
                if self.inp("Sicher? (ja/nein)").lower()=='ja' and self.crud.delete_user(uid): print("  ✅ Gelöscht!")
                input("\n  [Enter]...")
    
    # === SEARCH ===
    def m_search(self):
        while True:
            self.menu("SUCHEN", ["Spieler suchen","Teams suchen","Turniere suchen","Team-Matches"])
            c = self.choice(4)
            if c==0: return
            if c==1: self.table(self.search.search_players(self.inp("Suchbegriff")), ['player_id','nickname','team_name','role']); input("\n  [Enter]...")
            elif c==2: self.table(self.search.search_teams(self.inp("Suchbegriff")), ['team_id','team_name','abbreviation','country']); input("\n  [Enter]...")
            elif c==3:
                t = self.inp("Name/Ort",0) or None
                print("  Filter Tier: S-Tier, A-Tier, B-Tier, C-Tier (leer=alle)")
                tier = self.inp("Tier",0) or None
                print("  Filter Status: Upcoming, Ongoing, Completed, Cancelled (leer=alle)")
                status = self.inp("Status",0) or None
                self.table(self.search.search_tournaments(t, tier, status), ['tournament_id','tournament_name','tier','status'])
                input("\n  [Enter]...")
            elif c==4:
                for t in self.crud.get_all_teams(): print(f"    [{t['team_id']}] {t['team_name']}")
                self.table(self.search.search_matches_by_team(int(self.inp("\nTeam-ID"))), ['match_id','tournament_name','team1_name','score_team1','score_team2','team2_name'])
                input("\n  [Enter]...")
    
    # === EXPORT ===
    def m_export(self):
        while True:
            self.menu("EXPORT", ["Teams JSON","Teams CSV","Spieler JSON","Spieler CSV","Turniere JSON","Turniere CSV","Matches JSON","Matches CSV","Alles exportieren"])
            c = self.choice(9)
            if c==0: return
            opts = [(None,None),('TEAMS','json'),('TEAMS','csv'),('PLAYERS','json'),('PLAYERS','csv'),('TOURNAMENTS','json'),('TOURNAMENTS','csv'),('MATCHES','json'),('MATCHES','csv')]
            if c==9:
                for t in ['USERS','TEAMS','PLAYERS','TOURNAMENTS','MATCHES']:
                    self.exporter.export_table(t,'json'); self.exporter.export_table(t,'csv')
            elif c>0: self.exporter.export_table(*opts[c])
            input("\n  [Enter]...")
    
    # === IMPORT ===
    def m_import(self):
        while True:
            self.menu("IMPORT", ["Aus JSON","Aus CSV","Dateien anzeigen"])
            c = self.choice(3)
            if c==0: return
            if c==3:
                p = self.config.IMPORT_PATH
                if os.path.exists(p):
                    print(f"\n  📁 {p}\n")
                    for f in os.listdir(p): print(f"    - {f}")
                else: print(f"  Ordner nicht gefunden: {p}")
                input("\n  [Enter]...")
            else:
                fn = self.inp("Dateiname")
                fp = os.path.join(self.config.IMPORT_PATH, fn)
                print("  Tabellen: USERS, TEAMS, PLAYERS, TOURNAMENTS, MATCHES")
                t = self.inp("Zieltabelle")
                if c==1: self.importer.import_from_json(fp, t)
                else: self.importer.import_from_csv(fp, t)
                input("\n  [Enter]...")
    
    # === STATS ===
    def m_stats(self):
        self.header("STATISTIKEN")
        print(f"  📊 Teams: {len(self.crud.get_all_teams())}")
        print(f"  👥 Spieler: {len(self.crud.get_all_players())}")
        print(f"  🏆 Turniere: {len(self.crud.get_all_tournaments())}")
        print(f"  🎮 Matches: {len(self.crud.get_all_matches())}")
        print(f"  👤 Benutzer: {len(self.crud.get_all_users())}")
        print("\n  🏅 Top Teams nach Siegen:")
        for t in self.crud.get_all_teams()[:5]:
            s = self.search.get_team_statistics(t['team_id'])
            print(f"     {t['team_name']}: {s['total_wins']} Siege")
        input("\n  [Enter]...")

if __name__ == "__main__":
    CLI().run()

# CLAUDE.md - KI-Assistent-Leitfaden für Projekt_BTS

## Projektübersicht

**Projektname:** Projekt_BTS (BTS-Schulprojekt)
**Typ:** Esports-Event-Management-System
**Status:** 🚧 Vorentwicklung / Planungsphase
**Autor:** Quintic (Joeldenninger@proton.me)
**Zuletzt aktualisiert:** 2025-12-10

### Zweck
Dies ist ein Schulprojekt mit dem Ziel, eine umfassende Esports-Event-Management-Plattform mit folgenden Kernfunktionen zu entwickeln:

1. **Event-Organisation** - Werkzeuge zum Erstellen, Verwalten und Durchführen von Esports-Turnieren
2. **Vertrags-Management** - System zur Verwaltung von Spieler-/Team-Verträgen und Vereinbarungen
3. **Liga-System** - Strukturierter Liga-Spielbetrieb mit Major-Turnieren

## Aktueller Repository-Status

### Was bereits existiert
- ✅ Git-Repository initialisiert
- ✅ Basis-README.md mit Projektbeschreibung
- ✅ Saubere Git-History mit 6 Commits
- ✅ Remote-Repository konfiguriert

### Was noch fehlt
- ❌ Noch kein Quellcode vorhanden
- ❌ Kein Technology-Stack gewählt
- ❌ Keine Projektstruktur etabliert
- ❌ Keine Dependencies konfiguriert
- ❌ Kein Build-System eingerichtet
- ❌ Kein Testing-Framework
- ❌ Keine CI/CD-Pipeline
- ❌ Keine .gitignore-Datei
- ❌ Keine Entwicklungsumgebung eingerichtet

**Zeilenanzahl:** 0 (ohne Dokumentation)

## Repository-Struktur

```
Projekt_BTS/
├── .git/                    # Git-Versionskontrolle
├── README.md               # Projektbeschreibung (98 Bytes)
└── CLAUDE.md              # Diese Datei - KI-Assistent-Leitfaden
```

### Erwartete zukünftige Struktur

```
Projekt_BTS/
├── .github/
│   └── workflows/          # CI/CD-Pipelines
├── docs/                   # Zusätzliche Dokumentation
│   ├── api/               # API-Dokumentation
│   ├── architecture/      # Systemarchitektur-Dokumentation
│   └── guides/            # Entwicklungsanleitungen
├── src/                    # Quellcode
│   ├── backend/           # Backend-Services
│   │   ├── api/          # API-Endpunkte
│   │   ├── models/       # Datenmodelle
│   │   ├── services/     # Geschäftslogik
│   │   └── utils/        # Hilfsfunktionen
│   ├── frontend/          # Frontend-Anwendung
│   │   ├── components/   # UI-Komponenten
│   │   ├── pages/        # Seiten-Komponenten
│   │   ├── services/     # API-Clients
│   │   ├── hooks/        # Custom Hooks
│   │   └── utils/        # Frontend-Hilfsfunktionen
│   └── shared/            # Gemeinsamer Code zwischen Frontend/Backend
├── tests/                  # Test-Suites
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── scripts/                # Build- und Entwicklungs-Skripte
├── config/                 # Konfigurationsdateien
├── .gitignore             # Git-Ignore-Regeln
├── .env.example           # Umgebungsvariablen-Vorlage
├── README.md              # Projektübersicht
├── CLAUDE.md              # Diese Datei
└── [package.json|requirements.txt|etc.]  # Dependency-Management
```

## Technologie-Stack-Empfehlungen

### Entscheidungsstatus: ⏳ Noch nicht entschieden

Da noch kein Technologie-Stack gewählt wurde, sind hier empfohlene Optionen basierend auf den Projektanforderungen:

### Option 1: Moderner JavaScript/TypeScript-Stack (Empfohlen)
**Warum:** Industriestandard, großes Ökosystem, Full-Stack JavaScript

```yaml
Frontend:
  - Framework: React with TypeScript or Next.js
  - State Management: Zustand or Redux Toolkit
  - UI Library: shadcn/ui, Material-UI, or Tailwind CSS
  - API Client: TanStack Query (React Query)

Backend:
  - Runtime: Node.js with TypeScript
  - Framework: Express.js, Fastify, or NestJS
  - ORM: Prisma or TypeORM
  - Validation: Zod or Joi

Database:
  - PostgreSQL (empfohlen für relationale Daten)
  - Redis (für Caching und Sessions)

Testing:
  - Unit/Integration: Vitest or Jest
  - E2E: Playwright or Cypress
  - API Testing: Supertest

DevOps:
  - Containerization: Docker + Docker Compose
  - CI/CD: GitHub Actions
  - Deployment: Vercel/Railway/Render
```

### Option 2: Python-Stack
**Warum:** Großartig für schnelle Entwicklung, starke ML/Daten-Fähigkeiten

```yaml
Backend:
  - Framework: FastAPI or Django
  - ORM: SQLAlchemy or Django ORM
  - Validation: Pydantic

Frontend:
  - Wie Option 1 (React/TypeScript)

Database:
  - PostgreSQL

Testing:
  - pytest
  - pytest-asyncio
```

### Option 3: Java Enterprise Stack
**Warum:** Robust, Enterprise-tauglich, starke Typisierung

```yaml
Backend:
  - Framework: Spring Boot
  - Database Access: Spring Data JPA
  - Security: Spring Security

Frontend:
  - Wie Option 1 (React/TypeScript)

Database:
  - PostgreSQL

Testing:
  - JUnit 5
  - Mockito
  - Spring Test
```

## Entwicklungs-Workflows

### Git-Workflow

#### Branch-Strategie
- **Main Branch:** `main` oder `master` - Produktionsfertiger Code
- **Development Branch:** `dev` - Integrationsbranch für Features
- **Feature Branches:** `feature/<feature-name>` - Neue Features
- **Bug Fix Branches:** `fix/<bug-beschreibung>` - Bugfixes
- **Claude Branches:** `claude/claude-md-<session-id>` - KI-Assistent-Arbeit

#### Aktueller Branch
Arbeite an: `claude/claude-md-mizouigb4epwkeac-01Ti41tRC6hg8NJvbKpkPj3m`

#### Commit-Message-Konvention
Folge Conventional Commits:

```
<type>(<scope>): <betreff>

<body>

<footer>
```

**Typen:**
- `feat`: Neues Feature
- `fix`: Bugfix
- `docs`: Dokumentationsänderungen
- `style`: Code-Style-Änderungen (Formatierung, keine Logikänderung)
- `refactor`: Code-Refactoring
- `test`: Hinzufügen oder Aktualisieren von Tests
- `chore`: Wartungsaufgaben
- `perf`: Performance-Verbesserungen

**Beispiele:**
```
feat(events): event-erstellungs-endpunkt hinzugefügt
fix(contracts): datums-validierungsfehler behoben
docs(readme): installationsanweisungen aktualisiert
test(events): unit-tests für event-service hinzugefügt
```

### Entwicklungs-Setup (Sobald Tech-Stack gewählt ist)

#### Erstmalige Einrichtung
```bash
# Repository klonen
git clone <repository-url>
cd Projekt_BTS

# Dependencies installieren (Beispiel für Node.js)
npm install

# Umgebungs-Vorlage kopieren
cp .env.example .env

# Datenbank einrichten
npm run db:setup

# Migrationen ausführen
npm run db:migrate

# Entwicklungs-Server starten
npm run dev
```

#### Täglicher Entwicklungs-Workflow
```bash
# Lokales Repository aktualisieren
git fetch origin
git pull origin dev

# Feature-Branch erstellen
git checkout -b feature/mein-feature

# Änderungen vornehmen und häufig committen
git add .
git commit -m "feat(scope): beschreibung"

# Zum Remote pushen
git push -u origin feature/mein-feature

# Pull Request für Code-Review erstellen
```

## Code-Konventionen (Zu befolgen)

### Allgemeine Prinzipien

1. **Keep It Simple** - Vermeide Over-Engineering
2. **DRY** - Don't Repeat Yourself
3. **SOLID** - Folge SOLID-Prinzipien
4. **Test Coverage** - Strebe 80%+ Test-Abdeckung an
5. **Dokumentation** - Dokumentiere komplexe Logik und öffentliche APIs
6. **Type Safety** - Verwende TypeScript oder starke Typisierung wo möglich

### Datei-Benennung

```
TypeScript/JavaScript:
  - Components: PascalCase (EventCard.tsx)
  - Utilities: camelCase (formatDate.ts)
  - Constants: UPPER_SNAKE_CASE (API_ENDPOINTS.ts)
  - Types/Interfaces: PascalCase (Event.ts, IEventService.ts)

Python:
  - Modules: snake_case (event_service.py)
  - Classes: PascalCase
  - Functions: snake_case
  - Constants: UPPER_SNAKE_CASE

Java:
  - Classes: PascalCase (EventService.java)
  - Methods: camelCase
  - Constants: UPPER_SNAKE_CASE
```

### Code-Stil

#### TypeScript/JavaScript-Beispiel
```typescript
// Gut: Klar, typisiert, dokumentiert
/**
 * Erstellt ein neues Esports-Event
 * @param eventData - Event-Erstellungsparameter
 * @returns Erstelltes Event mit generierter ID
 */
export async function createEvent(
  eventData: CreateEventDto
): Promise<Event> {
  const validatedData = eventSchema.parse(eventData);
  return await eventRepository.create(validatedData);
}

// Schlecht: Keine Typen, keine Validierung, schlechte Benennung
export async function create(data) {
  return await db.events.insert(data);
}
```

#### Python-Beispiel
```python
# Gut: Type Hints, Docstrings, Validierung
async def create_event(event_data: CreateEventDto) -> Event:
    """
    Erstellt ein neues Esports-Event.

    Args:
        event_data: Event-Erstellungsparameter

    Returns:
        Erstelltes Event mit generierter ID

    Raises:
        ValidationError: Wenn Event-Daten ungültig sind
    """
    validated_data = validate_event_data(event_data)
    return await event_repository.create(validated_data)

# Schlecht: Keine Typen, keine Dokumentation
async def create(data):
    return await db.insert(data)
```

### Test-Konventionen

```typescript
// Unit-Test-Beispiel (Vitest/Jest)
describe('EventService', () => {
  describe('createEvent', () => {
    it('sollte Event mit gültigen Daten erstellen', async () => {
      const eventData = { name: 'Test-Turnier', date: '2025-12-15' };
      const result = await eventService.createEvent(eventData);

      expect(result).toHaveProperty('id');
      expect(result.name).toBe(eventData.name);
    });

    it('sollte Fehler bei ungültigem Datum werfen', async () => {
      const eventData = { name: 'Test', date: 'ungültig' };

      await expect(
        eventService.createEvent(eventData)
      ).rejects.toThrow('Ungültiges Datum');
    });
  });
});
```

## Feature-Entwicklungsbereiche

Basierend auf den Projektanforderungen sind hier die Hauptfunktionsbereiche zu implementieren:

### 1. Event-Management
**Priorität:** Hoch 🔴

**Features:**
- Event-Erstellung und -Konfiguration
- Turnier-Bracket-Management
- Match-Planung
- Live-Score-Tracking
- Event-Veröffentlichung und -Entdeckung
- Teilnehmer-Registrierung
- Event-Absage und -Umplanung

**Modelle:**
```typescript
interface Event {
  id: string;
  name: string;
  description: string;
  gameTitle: string;
  eventType: 'tournament' | 'league' | 'scrim';
  startDate: Date;
  endDate: Date;
  maxParticipants: number;
  currentParticipants: number;
  status: 'draft' | 'published' | 'ongoing' | 'completed' | 'cancelled';
  organizerId: string;
  prizePool?: number;
  rules?: string;
  brackets?: TournamentBracket;
}
```

### 2. Vertrags-Management
**Priorität:** Hoch 🔴

**Features:**
- Vertragserstellung und -vorlagen
- Digitale Signaturen
- Vertrags-Status-Tracking
- Vertragssuche und -filterung
- Vertrags-Ablauf-Benachrichtigungen
- Vertragsverlängerungs-Workflows
- Multi-Party-Verträge (Teams, Spieler, Organisationen)

**Modelle:**
```typescript
interface Contract {
  id: string;
  type: 'player' | 'team' | 'sponsor' | 'venue';
  title: string;
  parties: ContractParty[];
  startDate: Date;
  endDate: Date;
  status: 'draft' | 'pending_signatures' | 'active' | 'expired' | 'terminated';
  terms: ContractTerms;
  documents: Document[];
  signatures: Signature[];
  createdBy: string;
  createdAt: Date;
  updatedAt: Date;
}
```

### 3. Liga-System mit Majors
**Priorität:** Hoch 🔴

**Features:**
- Liga-Erstellung und -Konfiguration
- Saison-Management
- Divisions-/Tier-System
- Tabellen und Rankings
- Major-Turnier-Designation
- Aufstiegs-/Abstiegs-System
- Punkte- und Scoring-System
- Playoff-Brackets

**Modelle:**
```typescript
interface League {
  id: string;
  name: string;
  gameTitle: string;
  season: string;
  divisions: Division[];
  scoringSystem: ScoringRules;
  schedule: Match[];
  standings: TeamStanding[];
  majors: Major[];
  startDate: Date;
  endDate: Date;
  status: 'upcoming' | 'ongoing' | 'completed';
}

interface Major {
  id: string;
  leagueId: string;
  name: string;
  isMajor: true;
  prizePool: number;
  qualificationCriteria: QualificationRules;
  event: Event;
}
```

### 4. Benutzer- & Team-Management
**Priorität:** Mittel 🟡

**Features:**
- Benutzerregistrierung und -authentifizierung
- Benutzerprofile (Spieler, Organisatoren, Teams)
- Team-Erstellung und -Management
- Roster-Management
- Rollenbasierte Zugriffskontrolle
- Benutzer-Verifizierung

### 5. Zusätzliche Features
**Priorität:** Niedrig 🟢

**Features:**
- Benachrichtigungssystem
- E-Mail-Benachrichtigungen
- Live-Streaming-Integration
- Statistiken und Analytics
- Admin-Dashboard
- Content-Management
- Sponsoring-Management

## API-Design-Richtlinien

### RESTful-API-Konventionen

```
Events:
  GET    /api/events              - Liste aller Events
  GET    /api/events/:id          - Event-Details abrufen
  POST   /api/events              - Neues Event erstellen
  PUT    /api/events/:id          - Event aktualisieren
  DELETE /api/events/:id          - Event löschen
  POST   /api/events/:id/register - Für Event registrieren

Contracts:
  GET    /api/contracts           - Liste der Verträge
  GET    /api/contracts/:id       - Vertrags-Details abrufen
  POST   /api/contracts           - Vertrag erstellen
  PUT    /api/contracts/:id       - Vertrag aktualisieren
  POST   /api/contracts/:id/sign  - Vertrag unterschreiben

Leagues:
  GET    /api/leagues             - Liste der Ligen
  GET    /api/leagues/:id         - Liga-Details abrufen
  POST   /api/leagues             - Liga erstellen
  GET    /api/leagues/:id/standings - Tabelle abrufen
  GET    /api/leagues/:id/majors  - Liste der Major-Turniere
```

### Antwort-Format

```typescript
// Erfolgs-Antwort
{
  "success": true,
  "data": { /* Ressourcen-Daten */ },
  "message": "Event erfolgreich erstellt"
}

// Fehler-Antwort
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Ungültiges Event-Datum",
    "details": [
      {
        "field": "startDate",
        "message": "Startdatum muss in der Zukunft liegen"
      }
    ]
  }
}

// Paginierte Antwort
{
  "success": true,
  "data": [ /* Items */ ],
  "pagination": {
    "page": 1,
    "pageSize": 20,
    "totalPages": 5,
    "totalItems": 100
  }
}
```

## Datenbank-Design-Überlegungen

### Haupt-Entitäten

1. **Users** - Spieler, Organisatoren, Admins
2. **Teams** - Esports-Teams
3. **Events** - Turniere und Wettbewerbe
4. **Contracts** - Rechtliche Vereinbarungen
5. **Leagues** - Liga-Strukturen
6. **Matches** - Einzelne Spiele/Matches
7. **Organizations** - Unternehmen und Sponsoren

### Beziehungen

- Users → Teams (many-to-many via TeamMember)
- Teams → Events (many-to-many via Participation)
- Users/Teams → Contracts (many-to-many via ContractParty)
- Leagues → Events (one-to-many für Major-Turniere)
- Events → Matches (one-to-many)

### Indexierungs-Strategie

```sql
-- High-Priority-Indizes
CREATE INDEX idx_events_status ON events(status);
CREATE INDEX idx_events_start_date ON events(start_date);
CREATE INDEX idx_contracts_status ON contracts(status);
CREATE INDEX idx_contracts_end_date ON contracts(end_date);
CREATE INDEX idx_leagues_season ON leagues(season);
```

## Sicherheits-Überlegungen

### Authentifizierung & Autorisierung

1. **JWT-basierte Authentifizierung** für API-Zugriff
2. **Rollenbasierte Zugriffskontrolle (RBAC)**:
   - Admin: Voller System-Zugriff
   - Organizer: Events erstellen/verwalten
   - Player: Für Events registrieren, Verträge ansehen
   - Guest: Nur-Lese-Zugriff

### Datenschutz

- **Passwort-Hashing**: bcrypt oder Argon2
- **Input-Validierung**: Alle Benutzereingaben validieren
- **SQL-Injection-Prävention**: Parametrisierte Queries/ORM verwenden
- **XSS-Prävention**: Outputs sanitisieren
- **CSRF-Schutz**: CSRF-Tokens verwenden
- **Rate Limiting**: API-Missbrauch verhindern
- **Umgebungsvariablen**: Secrets in .env speichern (niemals committen)

### Sensible Daten

```bash
# .env.example (Vorlage - sicher zu committen)
DATABASE_URL=postgresql://user:password@localhost:5432/projekt_bts
JWT_SECRET=dein-geheimer-schlüssel-hier
JWT_EXPIRES_IN=7d
REDIS_URL=redis://localhost:6379
EMAIL_SERVICE=smtp.example.com
EMAIL_USER=noreply@example.com
EMAIL_PASSWORD=dein-email-passwort

# .env (tatsächlich - NIEMALS committen)
# Enthält echte Zugangsdaten
```

## KI-Assistent-Richtlinien

### Bei der Arbeit an diesem Projekt

1. **Immer zuerst lesen**
   - Lies bestehenden Code bevor du Änderungen vornimmst
   - Verstehe den Kontext und bestehende Muster
   - Prüfe auf ähnliche Implementierungen

2. **Folge etablierten Mustern**
   - Sobald ein Tech-Stack gewählt ist, folge seinen Konventionen
   - Passe dich an den bestehenden Code-Stil an
   - Verwende etablierte Benennungskonventionen

3. **Teste deine Änderungen**
   - Schreibe Tests für neue Features
   - Führe bestehende Tests vor dem Committen aus
   - Stelle sicher, dass es keine Regressionen gibt

4. **Dokumentiere unterwegs**
   - Aktualisiere diese CLAUDE.md wenn sich Muster ändern
   - Füge JSDoc/Docstrings für Funktionen hinzu
   - Aktualisiere API-Dokumentation

5. **Sicherheit zuerst**
   - Committe niemals Secrets oder Zugangsdaten
   - Validiere alle Eingaben
   - Folge Security-Best-Practices
   - Prüfe auf häufige Schwachstellen (OWASP Top 10)

6. **Keep It Simple**
   - Vermeide Over-Engineering
   - Mache minimale Änderungen um Probleme zu lösen
   - Refactorisiere nicht unabhängigen Code
   - Keine vorzeitige Optimierung

7. **Git-Hygiene**
   - Mache atomare Commits
   - Schreibe klare Commit-Messages
   - Halte Commits fokussiert auf eine Sache
   - Pushe zu geeigneten Feature-Branches

8. **Kommunikation**
   - Frage nach Klarstellung wenn Anforderungen unklar sind
   - Erkläre deinen Ansatz vor der Implementierung
   - Dokumentiere komplexe Entscheidungen

### Code-Review-Checkliste

Vor dem Committen überprüfen:

- [ ] Code folgt Projekt-Konventionen
- [ ] Tests bestehen (`npm test` oder Equivalent)
- [ ] Kein console.log oder Debug-Code übrig
- [ ] Keine Secrets oder Zugangsdaten im Code
- [ ] Typen sind korrekt definiert (TypeScript)
- [ ] Error-Handling ist implementiert
- [ ] Edge-Cases sind behandelt
- [ ] Dokumentation ist aktualisiert
- [ ] Keine unnötigen Dependencies hinzugefügt
- [ ] Code ist lesbar und wartbar

## Projekt-Initialisierungs-Schritte

### Phase 1: Setup (Aktuelle Priorität)

1. **Technologie-Stack wählen**
   - Entscheide dich für Frontend/Backend-Frameworks
   - Wähle Datenbank-System
   - Wähle Deployment-Plattform

2. **Projekt initialisieren**
   ```bash
   # Beispiel für Node.js/TypeScript
   npm init -y
   npm install typescript @types/node --save-dev
   npx tsc --init

   # Linting einrichten
   npm install eslint prettier --save-dev
   npx eslint --init

   # Testing einrichten
   npm install vitest @vitest/ui --save-dev
   ```

3. **Essentielle Dateien erstellen**
   - `.gitignore`
   - `.env.example`
   - `tsconfig.json` (falls TypeScript)
   - `docker-compose.yml`
   - Basis-Projektstruktur

4. **CI/CD einrichten**
   - Erstelle `.github/workflows/ci.yml`
   - Konfiguriere automatisiertes Testen
   - Richte Deployment-Pipeline ein

### Phase 2: Kern-Entwicklung

1. **Datenbank-Schema**
   - Entwerfe Entity-Relationship-Diagramm
   - Erstelle Migrations-Dateien
   - Richte Datenbank-Seeds ein

2. **Authentifizierungs-System**
   - Benutzerregistrierung/-login
   - JWT-Token-Management
   - Passwort-Reset-Flow

3. **Kern-Features** (in Reihenfolge)
   - Benutzerverwaltung
   - Event-Erstellung und -Management
   - Vertrags-System
   - Liga-System

### Phase 3: Verbesserung

1. **Erweiterte Features**
   - Benachrichtigungen
   - E-Mail-System
   - Analytics-Dashboard
   - Datei-Uploads

2. **Optimierung**
   - Performance-Tuning
   - Caching-Strategie
   - Datenbank-Optimierung

3. **Feinschliff**
   - UI/UX-Verbesserungen
   - Error-Handling
   - Loading-States
   - Barrierefreiheit

## Ressourcen & Referenzen

### Empfohlene Lektüre

- [Clean Code von Robert C. Martin](https://www.amazon.com/Clean-Code-Handbook-Software-Craftsmanship/dp/0132350882)
- [Refactoring von Martin Fowler](https://refactoring.com/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [REST API Design Best Practices](https://stackoverflow.blog/2020/03/02/best-practices-for-rest-api-design/)

### Nützliche Tools

- **API-Testing:** Postman, Insomnia, Thunder Client
- **Datenbank:** pgAdmin, DBeaver, MongoDB Compass
- **Versionskontrolle:** GitKraken, SourceTree, GitHub Desktop
- **Dokumentation:** Swagger/OpenAPI, Postman Collections
- **Monitoring:** Sentry, LogRocket, New Relic

## Kontakt & Support

**Projekt-Autor:** Quintic (Joeldenninger@proton.me)
**Repository:** JD68686727/Projekt_BTS
**Typ:** BTS-Schulprojekt

## Changelog

### 2025-12-10
- CLAUDE.md erstellt
- Projektumfang und -anforderungen dokumentiert
- Entwicklungs-Richtlinien etabliert
- Erwartete Architektur und Features definiert
- Vollständige Übersetzung ins Deutsche

---

**Hinweis:** Dieses Dokument ist lebendig und sollte aktualisiert werden, wenn sich das Projekt weiterentwickelt. Alle Entwickler und KI-Assistenten sollten diese Datei mit Projektänderungen, Konventionen und Mustern aktuell halten.

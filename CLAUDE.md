# CLAUDE.md - AI Assistant Guide for Projekt_BTS

## Project Overview

**Project Name:** Projekt_BTS (BTS School Project)
**Type:** Esports Event Management System
**Status:** 🚧 Pre-development / Planning Phase
**Author:** Quintic (Joeldenninger@proton.me)
**Last Updated:** 2025-12-10

### Purpose
This is a school project aimed at building a comprehensive esports event management platform with the following core features:

1. **Event Organization** - Tools for creating, managing, and hosting esports tournaments
2. **Contract Management** - System for handling player/team contracts and agreements
3. **League System** - Structured league play with major tournaments

## Current Repository State

### What Exists
- ✅ Git repository initialized
- ✅ Basic README.md with project description
- ✅ Clean git history with 6 commits
- ✅ Remote repository configured

### What's Missing
- ❌ No source code yet
- ❌ No technology stack chosen
- ❌ No project structure established
- ❌ No dependencies configured
- ❌ No build system set up
- ❌ No testing framework
- ❌ No CI/CD pipeline
- ❌ No .gitignore file
- ❌ No development environment setup

**Line Count:** 0 (excluding documentation)

## Repository Structure

```
Projekt_BTS/
├── .git/                    # Git version control
├── README.md               # Project description (98 bytes)
└── CLAUDE.md              # This file - AI assistant guide
```

### Expected Future Structure

```
Projekt_BTS/
├── .github/
│   └── workflows/          # CI/CD pipelines
├── docs/                   # Additional documentation
│   ├── api/               # API documentation
│   ├── architecture/      # System architecture docs
│   └── guides/            # Development guides
├── src/                    # Source code
│   ├── backend/           # Backend services
│   │   ├── api/          # API endpoints
│   │   ├── models/       # Data models
│   │   ├── services/     # Business logic
│   │   └── utils/        # Utility functions
│   ├── frontend/          # Frontend application
│   │   ├── components/   # UI components
│   │   ├── pages/        # Page components
│   │   ├── services/     # API clients
│   │   ├── hooks/        # Custom hooks
│   │   └── utils/        # Frontend utilities
│   └── shared/            # Shared code between frontend/backend
├── tests/                  # Test suites
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── scripts/                # Build and development scripts
├── config/                 # Configuration files
├── .gitignore             # Git ignore rules
├── .env.example           # Environment variable template
├── README.md              # Project overview
├── CLAUDE.md              # This file
└── [package.json|requirements.txt|etc.]  # Dependency management
```

## Technology Stack Recommendations

### Decision Status: ⏳ Not Yet Decided

Since no technology stack has been chosen, here are recommended options based on the project requirements:

### Option 1: Modern JavaScript/TypeScript Stack (Recommended)
**Why:** Industry standard, large ecosystem, full-stack JavaScript

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
  - PostgreSQL (recommended for relational data)
  - Redis (for caching and sessions)

Testing:
  - Unit/Integration: Vitest or Jest
  - E2E: Playwright or Cypress
  - API Testing: Supertest

DevOps:
  - Containerization: Docker + Docker Compose
  - CI/CD: GitHub Actions
  - Deployment: Vercel/Railway/Render
```

### Option 2: Python Stack
**Why:** Great for rapid development, strong ML/data capabilities

```yaml
Backend:
  - Framework: FastAPI or Django
  - ORM: SQLAlchemy or Django ORM
  - Validation: Pydantic

Frontend:
  - Same as Option 1 (React/TypeScript)

Database:
  - PostgreSQL

Testing:
  - pytest
  - pytest-asyncio
```

### Option 3: Java Enterprise Stack
**Why:** Robust, enterprise-grade, strong typing

```yaml
Backend:
  - Framework: Spring Boot
  - Database Access: Spring Data JPA
  - Security: Spring Security

Frontend:
  - Same as Option 1 (React/TypeScript)

Database:
  - PostgreSQL

Testing:
  - JUnit 5
  - Mockito
  - Spring Test
```

## Development Workflows

### Git Workflow

#### Branch Strategy
- **Main Branch:** `main` or `master` - Production-ready code
- **Development Branch:** `dev` - Integration branch for features
- **Feature Branches:** `feature/<feature-name>` - New features
- **Bug Fix Branches:** `fix/<bug-description>` - Bug fixes
- **Claude Branches:** `claude/claude-md-<session-id>` - AI assistant work

#### Current Branch
Working on: `claude/claude-md-mizouigb4epwkeac-01Ti41tRC6hg8NJvbKpkPj3m`

#### Commit Message Convention
Follow conventional commits:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, no logic change)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks
- `perf`: Performance improvements

**Examples:**
```
feat(events): add event creation endpoint
fix(contracts): resolve date validation bug
docs(readme): update installation instructions
test(events): add unit tests for event service
```

### Development Setup (Once Tech Stack is Chosen)

#### First Time Setup
```bash
# Clone repository
git clone <repository-url>
cd Projekt_BTS

# Install dependencies (example for Node.js)
npm install

# Copy environment template
cp .env.example .env

# Set up database
npm run db:setup

# Run migrations
npm run db:migrate

# Start development server
npm run dev
```

#### Daily Development Workflow
```bash
# Update local repository
git fetch origin
git pull origin dev

# Create feature branch
git checkout -b feature/my-feature

# Make changes and commit frequently
git add .
git commit -m "feat(scope): description"

# Push to remote
git push -u origin feature/my-feature

# Create pull request for code review
```

## Code Conventions (To Be Followed)

### General Principles

1. **Keep It Simple** - Avoid over-engineering
2. **DRY** - Don't Repeat Yourself
3. **SOLID** - Follow SOLID principles
4. **Test Coverage** - Aim for 80%+ test coverage
5. **Documentation** - Document complex logic and public APIs
6. **Type Safety** - Use TypeScript or strong typing wherever possible

### File Naming

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

### Code Style

#### TypeScript/JavaScript Example
```typescript
// Good: Clear, typed, documented
/**
 * Creates a new esports event
 * @param eventData - Event creation parameters
 * @returns Created event with generated ID
 */
export async function createEvent(
  eventData: CreateEventDto
): Promise<Event> {
  const validatedData = eventSchema.parse(eventData);
  return await eventRepository.create(validatedData);
}

// Bad: No types, no validation, poor naming
export async function create(data) {
  return await db.events.insert(data);
}
```

#### Python Example
```python
# Good: Type hints, docstrings, validation
async def create_event(event_data: CreateEventDto) -> Event:
    """
    Creates a new esports event.

    Args:
        event_data: Event creation parameters

    Returns:
        Created event with generated ID

    Raises:
        ValidationError: If event data is invalid
    """
    validated_data = validate_event_data(event_data)
    return await event_repository.create(validated_data)

# Bad: No types, no docs
async def create(data):
    return await db.insert(data)
```

### Testing Conventions

```typescript
// Unit Test Example (Vitest/Jest)
describe('EventService', () => {
  describe('createEvent', () => {
    it('should create event with valid data', async () => {
      const eventData = { name: 'Test Tournament', date: '2025-12-15' };
      const result = await eventService.createEvent(eventData);

      expect(result).toHaveProperty('id');
      expect(result.name).toBe(eventData.name);
    });

    it('should throw error with invalid date', async () => {
      const eventData = { name: 'Test', date: 'invalid' };

      await expect(
        eventService.createEvent(eventData)
      ).rejects.toThrow('Invalid date');
    });
  });
});
```

## Feature Development Areas

Based on the project requirements, here are the key feature areas to implement:

### 1. Event Management
**Priority:** High 🔴

**Features:**
- Event creation and configuration
- Tournament bracket management
- Match scheduling
- Live score tracking
- Event publishing and discovery
- Participant registration
- Event cancellation and rescheduling

**Models:**
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

### 2. Contract Management
**Priority:** High 🔴

**Features:**
- Contract creation and templates
- Digital signatures
- Contract status tracking
- Contract search and filtering
- Contract expiration notifications
- Contract renewal workflows
- Multi-party contracts (teams, players, organizations)

**Models:**
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

### 3. League System with Majors
**Priority:** High 🔴

**Features:**
- League creation and configuration
- Season management
- Division/tier system
- Standings and rankings
- Major tournament designation
- Promotion/relegation system
- Points and scoring system
- Playoff brackets

**Models:**
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

### 4. User & Team Management
**Priority:** Medium 🟡

**Features:**
- User registration and authentication
- User profiles (players, organizers, teams)
- Team creation and management
- Roster management
- Role-based access control
- User verification

### 5. Additional Features
**Priority:** Low 🟢

**Features:**
- Notifications system
- Email notifications
- Live streaming integration
- Statistics and analytics
- Admin dashboard
- Content management
- Sponsorship management

## API Design Guidelines

### RESTful API Conventions

```
Events:
  GET    /api/events              - List all events
  GET    /api/events/:id          - Get event details
  POST   /api/events              - Create new event
  PUT    /api/events/:id          - Update event
  DELETE /api/events/:id          - Delete event
  POST   /api/events/:id/register - Register for event

Contracts:
  GET    /api/contracts           - List contracts
  GET    /api/contracts/:id       - Get contract details
  POST   /api/contracts           - Create contract
  PUT    /api/contracts/:id       - Update contract
  POST   /api/contracts/:id/sign  - Sign contract

Leagues:
  GET    /api/leagues             - List leagues
  GET    /api/leagues/:id         - Get league details
  POST   /api/leagues             - Create league
  GET    /api/leagues/:id/standings - Get standings
  GET    /api/leagues/:id/majors  - List major tournaments
```

### Response Format

```typescript
// Success Response
{
  "success": true,
  "data": { /* resource data */ },
  "message": "Event created successfully"
}

// Error Response
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid event date",
    "details": [
      {
        "field": "startDate",
        "message": "Start date must be in the future"
      }
    ]
  }
}

// Paginated Response
{
  "success": true,
  "data": [ /* items */ ],
  "pagination": {
    "page": 1,
    "pageSize": 20,
    "totalPages": 5,
    "totalItems": 100
  }
}
```

## Database Design Considerations

### Key Entities

1. **Users** - Players, organizers, admins
2. **Teams** - Esports teams
3. **Events** - Tournaments and competitions
4. **Contracts** - Legal agreements
5. **Leagues** - League structures
6. **Matches** - Individual games/matches
7. **Organizations** - Companies and sponsors

### Relationships

- Users → Teams (many-to-many via TeamMember)
- Teams → Events (many-to-many via Participation)
- Users/Teams → Contracts (many-to-many via ContractParty)
- Leagues → Events (one-to-many for major tournaments)
- Events → Matches (one-to-many)

### Indexing Strategy

```sql
-- High-priority indexes
CREATE INDEX idx_events_status ON events(status);
CREATE INDEX idx_events_start_date ON events(start_date);
CREATE INDEX idx_contracts_status ON contracts(status);
CREATE INDEX idx_contracts_end_date ON contracts(end_date);
CREATE INDEX idx_leagues_season ON leagues(season);
```

## Security Considerations

### Authentication & Authorization

1. **JWT-based authentication** for API access
2. **Role-based access control (RBAC)**:
   - Admin: Full system access
   - Organizer: Create/manage events
   - Player: Register for events, view contracts
   - Guest: Read-only access

### Data Protection

- **Password hashing**: bcrypt or Argon2
- **Input validation**: Validate all user inputs
- **SQL injection prevention**: Use parameterized queries/ORM
- **XSS prevention**: Sanitize outputs
- **CSRF protection**: Use CSRF tokens
- **Rate limiting**: Prevent API abuse
- **Environment variables**: Store secrets in .env (never commit)

### Sensitive Data

```bash
# .env.example (template - safe to commit)
DATABASE_URL=postgresql://user:password@localhost:5432/projekt_bts
JWT_SECRET=your-secret-key-here
JWT_EXPIRES_IN=7d
REDIS_URL=redis://localhost:6379
EMAIL_SERVICE=smtp.example.com
EMAIL_USER=noreply@example.com
EMAIL_PASSWORD=your-email-password

# .env (actual - NEVER commit)
# Contains real credentials
```

## AI Assistant Guidelines

### When Working on This Project

1. **Always Read First**
   - Read existing code before making changes
   - Understand the context and existing patterns
   - Check for similar implementations

2. **Follow Established Patterns**
   - Once a tech stack is chosen, follow its conventions
   - Match existing code style
   - Use established naming conventions

3. **Test Your Changes**
   - Write tests for new features
   - Run existing tests before committing
   - Ensure no regressions

4. **Document as You Go**
   - Update this CLAUDE.md when patterns change
   - Add JSDoc/docstrings for functions
   - Update API documentation

5. **Security First**
   - Never commit secrets or credentials
   - Validate all inputs
   - Follow security best practices
   - Check for common vulnerabilities (OWASP Top 10)

6. **Keep It Simple**
   - Avoid over-engineering
   - Make minimal changes to fix issues
   - Don't refactor unrelated code
   - No premature optimization

7. **Git Hygiene**
   - Make atomic commits
   - Write clear commit messages
   - Keep commits focused on one thing
   - Push to appropriate feature branches

8. **Communication**
   - Ask for clarification when requirements are unclear
   - Explain your approach before implementing
   - Document complex decisions

### Code Review Checklist

Before committing, verify:

- [ ] Code follows project conventions
- [ ] Tests pass (`npm test` or equivalent)
- [ ] No console.log or debug code left in
- [ ] No secrets or credentials in code
- [ ] Types are properly defined (TypeScript)
- [ ] Error handling is implemented
- [ ] Edge cases are handled
- [ ] Documentation is updated
- [ ] No unnecessary dependencies added
- [ ] Code is readable and maintainable

## Project Initialization Steps

### Phase 1: Setup (Current Priority)

1. **Choose Technology Stack**
   - Decide on frontend/backend frameworks
   - Select database system
   - Choose deployment platform

2. **Initialize Project**
   ```bash
   # Example for Node.js/TypeScript
   npm init -y
   npm install typescript @types/node --save-dev
   npx tsc --init

   # Set up linting
   npm install eslint prettier --save-dev
   npx eslint --init

   # Set up testing
   npm install vitest @vitest/ui --save-dev
   ```

3. **Create Essential Files**
   - `.gitignore`
   - `.env.example`
   - `tsconfig.json` (if TypeScript)
   - `docker-compose.yml`
   - Basic project structure

4. **Set Up CI/CD**
   - Create `.github/workflows/ci.yml`
   - Configure automated testing
   - Set up deployment pipeline

### Phase 2: Core Development

1. **Database Schema**
   - Design entity relationship diagram
   - Create migration files
   - Set up database seeds

2. **Authentication System**
   - User registration/login
   - JWT token management
   - Password reset flow

3. **Core Features** (in order)
   - User management
   - Event creation and management
   - Contract system
   - League system

### Phase 3: Enhancement

1. **Advanced Features**
   - Notifications
   - Email system
   - Analytics dashboard
   - File uploads

2. **Optimization**
   - Performance tuning
   - Caching strategy
   - Database optimization

3. **Polish**
   - UI/UX improvements
   - Error handling
   - Loading states
   - Accessibility

## Resources & References

### Recommended Reading

- [Clean Code by Robert C. Martin](https://www.amazon.com/Clean-Code-Handbook-Software-Craftsmanship/dp/0132350882)
- [Refactoring by Martin Fowler](https://refactoring.com/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [REST API Design Best Practices](https://stackoverflow.blog/2020/03/02/best-practices-for-rest-api-design/)

### Useful Tools

- **API Testing:** Postman, Insomnia, Thunder Client
- **Database:** pgAdmin, DBeaver, MongoDB Compass
- **Version Control:** GitKraken, SourceTree, GitHub Desktop
- **Documentation:** Swagger/OpenAPI, Postman Collections
- **Monitoring:** Sentry, LogRocket, New Relic

## Contact & Support

**Project Author:** Quintic (Joeldenninger@proton.me)
**Repository:** JD68686727/Projekt_BTS
**Type:** BTS School Project

## Changelog

### 2025-12-10
- Created CLAUDE.md
- Documented project scope and requirements
- Established development guidelines
- Defined expected architecture and features

---

**Note:** This document is living and should be updated as the project evolves. All developers and AI assistants should keep this file current with project changes, conventions, and patterns.

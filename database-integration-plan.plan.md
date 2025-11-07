<!-- 99d8731c-051f-459b-88d5-aa8d69803dbf fdbaa640-63df-4464-8d63-302df0edfff4 -->
## Database Integration and Authentication Implementation Plan

### Overview

This plan will guide you through completing Milestone 3 requirements while preparing for Milestone 4. You'll implement a MySQL database connection, create necessary SQL schemas with advanced features, and replace the JSON test data with real database operations. Everything stays intro-level and straightforward.

### Key context tie-ins
- Uses your existing Flask app structure and templates without overhauling UI.
- Replaces JSON mocks with SQLAlchemy queries that return the same shapes your templates expect.
- Implements the exact advanced SQL features you selected: Trigger + Stored Procedure + CHECK constraints.

### Phase 0 — Map ERD to concrete tables and columns
Tables from `Chill Study Sesh App Flow.drawio.html` (ERD), turned into SQLAlchemy-friendly schema names and fields.

- user
  - user_id (PK, int)
  - email (varchar 50, unique)
  - password_hash (varchar 255)
  - first_name (varchar 50)
  - last_name (varchar 50)
  - phone (varchar 20, optional)
  - created_at (timestamp default now)
- course_offering
  - course_offering_id (PK, int)
  - title (varchar 100)
  - section (varchar 20)
  - year (int)
  - term (int CHECK 1..3)
  - created_by_user (FK → user.user_id)
- location
  - location_id (PK, int)
  - address (varchar 100)
  - room_number (varchar 20)
  - created_by_user (FK → user.user_id)
- room_type
  - room_type_id (PK, int)
  - type_name (varchar 20)
  - description (text)
- study_session
  - session_id (PK, int)
  - course_offering_id (FK → course_offering.course_offering_id)
  - location_id (FK → location.location_id)
  - organizer_id (FK → user.user_id)
  - max_attendees (int CHECK > 0)
  - description (varchar 200)
  - start_time (timestamp)
  - end_time (timestamp)
  - chill_level (int CHECK 1..3)
  - room_type_id (FK → room_type.room_type_id, nullable)
- attendance (junction: user attends session)
  - user_id (FK → user.user_id)
  - session_id (FK → study_session.session_id)
  - PRIMARY KEY (user_id, session_id)
- tag
  - tag_id (PK, int)
  - tag_name (varchar 50)
- session_tag (junction: session has tag)
  - session_id (FK → study_session.session_id)
  - tag_id (FK → tag.tag_id)
  - PRIMARY KEY (session_id, tag_id)
- resource
  - resource_id (PK, int)
  - session_id (FK → study_session.session_id)
  - uploaded_by (FK → user.user_id)
  - resource_name (varchar 50)
  - resource_url (text)
- reminder
  - reminder_id (PK, int)
  - user_id (FK → user.user_id)
  - session_id (FK → study_session.session_id)
  - reminder_time (timestamp)
  - reminder_sent (boolean default false)

### Phase 1: Database Setup and Configuration

#### 1.1 Install Required Dependencies

Add to `requirements.txt`:

- `Flask-SQLAlchemy==3.1.1`
- `PyMySQL==1.1.0`
- `Flask-Login==0.6.3`
- `python-dotenv==1.0.0`

#### 1.2 Environment Configuration

Create `.env` file for local development with database credentials (to be added to Render later):

- `DATABASE_HOST`
- `DATABASE_USER`
- `DATABASE_PASSWORD`
- `DATABASE_NAME`
- `SECRET_KEY`

Update `config.py` to read from environment variables and build MySQL connection string.

Example (to be implemented):

```python
import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-production")

    host = os.environ.get("DATABASE_HOST")
    user = os.environ.get("DATABASE_USER")
    pwd = os.environ.get("DATABASE_PASSWORD")
    name = os.environ.get("DATABASE_NAME")

    if host and user and pwd and name:
        SQLALCHEMY_DATABASE_URI = (
            f"mysql+pymysql://{user}:{pwd}@{host}/{name}?charset=utf8mb4"
        )
    else:
        SQLALCHEMY_DATABASE_URI = "sqlite:///chill_study.db"

    SQLALCHEMY_TRACK_MODIFICATIONS = False
```

Render environment variables:
- `DATABASE_HOST`, `DATABASE_USER`, `DATABASE_PASSWORD`, `DATABASE_NAME`, `SECRET_KEY`, `PYTHON_VERSION=3.12.3`.

Hostinger: ensure remote connections are allowed for your MySQL user (host `%` or specific IP). If SSL is required, we’ll add SSL options later (keep off for simplicity if not required).

#### 1.3 Initialize SQLAlchemy

Create `models.py` to define database models based on your ERD:

- User model
- StudySession model
- Attendance model (junction table)
- Location model
- CourseOffering model
- Tag model
- SessionTag model (junction table)
- Resource model
- Reminder model
- RoomType model

### Phase 2: SQL Schema Creation with Advanced Features

#### 2.1 Create Database Schema SQL File

Generate `schema.sql` with:

- All CREATE TABLE statements matching your models
- Primary keys, foreign keys, constraints
- Proper data types and NULL/NOT NULL specifications

#### 2.2 Implement Advanced SQL Features (Milestone 3 Requirement)

**CHECK Constraint:**

- Add CHECK constraint on `study_session.max_attendees` (must be > 0)
- Add CHECK constraint on `study_session.chill_level` (must be 1-3)
- Add CHECK constraint on `course_offering.term` (must be 1-3)

**Trigger:**

- Create trigger `before_attendance_insert` that prevents users from joining sessions that are at max capacity
- (Optional) Organizer auto-attendance can be enforced in app code (intro-level)

**Stored Procedure:**

- Create procedure `cleanup_old_reminders` that deletes reminders older than 30 days where `reminder_sent = TRUE`
- Create procedure `get_user_sessions` that retrieves all sessions for a given user ID

#### 2.3 Data Population Guide

Create SQL INSERT templates and a guide document for you to:

- Convert existing JSON test data to SQL INSERT statements
- Learn how to manually enter data via SQL
- Understand the relationships between tables

### Phase 3: Replace JSON with Database Operations

#### 3.1 Update Application Factory (`__init__.py`)

- Initialize SQLAlchemy with app
- Initialize Flask-Login
- Create database tables on first run (for dev only)

#### 3.2 Refactor Routes (`routes.py`)

Replace each JSON data operation:

**Retrieve Operations:**

- Dashboard: Query user's sessions via Attendance relationship
- Session details: Query by session ID with relationships
- Available sessions: Query sessions with filters

**Create Operations:**

- Create session: Use SQLAlchemy `db.session.add()` and commit
- Join session: Create Attendance record
- Add location/course: Create and commit new records

**Update Operations:**

- Update session details
- Mark reminders as sent

**Delete Operations:**

- Leave session: Delete Attendance record
- (Keep it simple - soft deletes not required for intro level)

#### 3.3 Remove Test Data Files

Delete all files in `tests/` directory:

- `course_offering_data.py`
- `join_session_data.py`
- `location_data.py`
- `my_session_data.py`
- `reminder_data.py`
- `resource_data.py`
- `room_type_data.py`
- `tag_data.py`

### Phase 4: Basic Authentication (Milestone 4 Requirement)

#### 4.1 Implement User Model Extensions

Add Flask-Login required methods to User model:

- `get_id()` (or inherit from `UserMixin`)

#### 4.2 Password Hashing

Use `werkzeug.security`:

- `generate_password_hash()` for registration
- `check_password_hash()` for login

#### 4.3 Update Authentication Routes

Implement proper login/logout/register functionality:

- Login: Validate credentials, use `login_user()`
- Logout: Use `logout_user()`
- Register: Hash password, create user, auto-login

#### 4.4 Protect Routes

Add `@login_required` decorator to routes that need authentication:

- Dashboard
- Create session
- Join/leave session
- All session management routes

### Phase 5: Testing and Documentation

#### 5.1 Local Testing Checklist

Test all CRUD operations:

- [ ] User registration and login
- [ ] Create study session
- [ ] View sessions (own and available)
- [ ] Join session
- [ ] Leave session
- [ ] Add locations and courses
- [ ] Upload resources
- [ ] Set reminders

#### 5.2 Render Deployment Setup

- Add environment variables in Render dashboard
- Deploy updated application
- Run database initialization (prefer phpMyAdmin running `schema.sql`)
- Test deployed application

#### 5.3 Milestone 3 Documentation

Prepare report sections:

1. Database server info (Hostinger details)
2. Table schemas (DESC commands screenshots)
3. Row counts (SELECT COUNT(*) screenshots)
4. Sample data (SELECT * screenshots showing 10+ rows)
5. SQL commands documentation:

- CREATE TABLE statements
- All CRUD queries used in app
- Advanced SQL (triggers, procedures, constraints)

### Key Files to Create/Modify

**New Files:**

- `models.py` - SQLAlchemy models
- `.env` - Environment variables (local)
- `schema.sql` - Complete database schema with advanced features
- `data_population_guide.md` - Instructions for entering test data
- `migrations/` - (optional) Database migration scripts

**Modified Files:**

- `requirements.txt` - Add new dependencies
- `config.py` - Database configuration
- `__init__.py` - Initialize extensions
- `routes.py` - Replace all JSON operations with database queries
- `app.py` - (minimal changes if any)

**Deleted:**

- All files in `tests/` directory

### Important Notes

1. **Intro-Level Approach**: All code will be straightforward with clear comments. No complex ORM patterns or advanced SQLAlchemy features.
2. **Framework Provided**: Models, routes, and SQL will be 80% complete. You'll fill in simple parts like:
   - Additional field validations
   - Some query filters
   - Simple route logic
3. **Testing**: Test locally first before deploying to Render. Use MySQL Workbench or phpMyAdmin to verify database operations.
4. **Milestone 3 Requirements Met**:
   - ✅ MySQL database setup
   - ✅ All tables from ERD
   - ✅ 10+ entries per table (you'll add via guide)
   - ✅ All CRUD SQL commands
   - ✅ 3 different advanced PL/SQL features
   - ✅ Proper testing and verification
5. **Milestone 4 Preparation**:
   - ✅ Database programming complete
   - ✅ All functionalities implemented
   - ✅ Multi-user support via shared database
   - ✅ Basic authentication at application level
   - ✅ Returning user support via login

### Hostinger / Render specifics

- Hostinger MySQL remote access:
  - Allow remote connections for your MySQL user (`%` host or specific IPs). If using Render free tier, IPs may change; test locally first. For grading, temporarily open `%` if needed.
- Render service config:
  - Build command: `pip install -r requirements.txt`
  - Start command: `gunicorn app:app`
  - Environment: set the DB variables + `SECRET_KEY`.
- First run strategy:
  - Prefer running `schema.sql` via phpMyAdmin on Hostinger (ensures triggers/procedures/check constraints exist as defined).
  - In development, `db.create_all()` can create base tables, but won’t create triggers/procedures/checks.

### Advanced SQL snippets (for `schema.sql` via phpMyAdmin)

CHECK constraints examples:

```sql
-- inside CREATE TABLE study_session
CHECK (max_attendees > 0),
CHECK (chill_level in (1,2,3))
```

```sql
-- inside CREATE TABLE course_offering
CHECK (term in (1,2,3))
```

Trigger (capacity limit):

```sql
DELIMITER //
CREATE TRIGGER before_attendance_insert
BEFORE INSERT ON attendance
FOR EACH ROW
BEGIN
  DECLARE current_count INT;
  DECLARE max_cap INT;
  SELECT COUNT(*) INTO current_count FROM attendance WHERE session_id = NEW.session_id;
  SELECT max_attendees INTO max_cap FROM study_session WHERE session_id = NEW.session_id;
  IF current_count >= max_cap THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Session is at capacity';
  END IF;
END//
DELIMITER ;
```

Stored procedures:

```sql
DELIMITER //
CREATE PROCEDURE cleanup_old_reminders()
BEGIN
  DELETE FROM reminder
  WHERE reminder_sent = 1
    AND reminder_time < (NOW() - INTERVAL 30 DAY);
END//

CREATE PROCEDURE get_user_sessions(IN p_user_id INT)
BEGIN
  SELECT s.*
  FROM study_session s
  LEFT JOIN attendance a ON a.session_id = s.session_id
  WHERE s.organizer_id = p_user_id OR a.user_id = p_user_id
  GROUP BY s.session_id;
END//
DELIMITER ;
```

DB security (minimum privileges for app user):

```sql
CREATE USER 'app_user'@'%' IDENTIFIED BY 'yourStrongPassword';
GRANT SELECT, INSERT, UPDATE, DELETE ON your_db_name.* TO 'app_user'@'%';
FLUSH PRIVILEGES;
```

### Phase 6 — Data population (you do it, with structured guidance)

Create `data_population_guide.md` with ready-to-edit INSERT templates. Example snippets you’ll fill in and run in phpMyAdmin:

```sql
-- user (≥ 10 rows)
INSERT INTO user (email, password_hash, first_name, last_name, phone)
VALUES ('alice@example.com', '<hash>', 'Alice', 'Morgan', '5551231234');

-- course_offering
INSERT INTO course_offering (title, section, year, term, created_by_user)
VALUES ('Principles Of Database Systems', 'A', 2025, 1, 1);

-- location
INSERT INTO location (address, room_number, created_by_user)
VALUES ('Main Library', '101', 1);

-- room_type
INSERT INTO room_type (type_name, description)
VALUES ('Quiet', 'Quiet room');

-- study_session (organizer_id should be a valid user_id)
INSERT INTO study_session (course_offering_id, location_id, organizer_id, max_attendees, description, start_time, end_time, chill_level, room_type_id)
VALUES (1, 1, 1, 20, 'ER modeling review', '2025-02-18 07:00:00', '2025-02-18 09:00:00', 1, 1);

-- attendance
INSERT INTO attendance (user_id, session_id) VALUES (2, 1);

-- tag
INSERT INTO tag (tag_name) VALUES ('Group Work');

-- session_tag
INSERT INTO session_tag (session_id, tag_id) VALUES (1, 1);

-- resource
INSERT INTO resource (session_id, uploaded_by, resource_name, resource_url)
VALUES (1, 1, 'ER_Problems.pdf', 'https://cdn.example.com/ER_Problems.pdf');

-- reminder
INSERT INTO reminder (user_id, session_id, reminder_time, reminder_sent)
VALUES (1, 1, '2025-02-17 20:00:00', 0);
```

After population, capture required screenshots for Milestone 3:
- `DESC table-name`
- `SELECT COUNT(*) FROM table-name;`
- `SELECT * FROM table-name LIMIT 10;`

### Phase 7 — Replace JSON mocks with DB queries (surgical refactor)

Your routes currently import Python lists from `tests/` modules; remove these imports and replace with SQLAlchemy queries.

Refactors:
- Dashboard/home:
  - my_sessions: sessions where `current_user` is in attendance OR organizer
  - join_sessions: sessions not attended by `current_user` (and optional time filter)
  - include related course/location/room_type, tags, resources, reminders via relationships
- Create session (POST):
  - insert `StudySession`, then auto-add `Attendance` for organizer
- View session: load by id; map ORM → dict to keep templates unchanged
- Upload resource: insert `Resource` with `uploaded_by=current_user`
- Leave session: delete `Attendance` for (current_user, session)
- `/api/locations` and `/api/courses` GET/POST: implement simple SELECT/INSERT with filters

Small adapter helpers will transform ORM models to the dict shape your templates expect.

### Phase 8 — Milestone 4-grade-aligned features

- Sorting/filtering/searching: leverage existing endpoints with SQL-backed filters; optionally add `sort` or `q` params.
- Export: add `/api/sessions/export?format=json` that returns JSON from a query (easy graded point).
- Concurrent users: Render + Hostinger shared DB satisfies requirement.
- Security: DB GRANTs + Flask-Login with password hashing.

### Minimal code changes mapped to your files

- `requirements.txt`: add packages listed above
- `config.py`: build MySQL URL from envs; fallback to sqlite
- `models.py`: all models and relationships
- `__init__.py`: init db, login manager, `user_loader`, optionally `db.create_all()`
- `routes.py`: remove `tests/` imports; replace with ORM queries and adapters
- `app.py`: unchanged
- Delete `tests/` data files (once DB is fully in place)

### To-dos

- [ ] Install required packages (SQLAlchemy, PyMySQL, Flask-Login, python-dotenv)
- [ ] Create .env file and update config.py with database connection
- [ ] Create models.py with all SQLAlchemy models from ERD
- [ ] Generate schema.sql with CREATE TABLE statements
- [ ] Add CHECK constraints to schema.sql for validation
- [ ] Write SQL trigger for attendance capacity checking
- [ ] Write stored procedures for cleanup and queries
- [ ] Create guide for manually entering test data
- [ ] Update __init__.py to initialize SQLAlchemy and Flask-Login
- [ ] Replace JSON data with database queries for retrieving data
- [ ] Replace JSON operations with database INSERT operations
- [ ] Implement UPDATE and DELETE database operations
- [ ] Delete all JSON test data files from tests/ directory
- [ ] Add Flask-Login methods to User model
- [ ] Add password hashing for registration and login
- [ ] Implement proper login, logout, and register functionality
- [ ] Add @login_required decorators to protected routes
- [ ] Test all CRUD operations locally
- [ ] Deploy to Render with environment variables
- [ ] Prepare Milestone 3 documentation with screenshots and SQL commands



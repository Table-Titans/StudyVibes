CREATE TABLE User (
    user_id INT PRIMARY KEY,
    email VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    phone INT,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE CourseOffering (
    course_offering_id INT PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    section VARCHAR(20),
    year INT,
    term INT CHECK (term BETWEEN 1 AND 4), #nyu has a winter term so 4 seasons
    created_by_user INT,
    FOREIGN KEY (created_by_user) REFERENCES User(user_id)
);

CREATE TABLE Location (
    location_id INT PRIMARY KEY,
    address VARCHAR(100),
    room_number VARCHAR(20),
    created_by_user INT,
    FOREIGN KEY (created_by_user) REFERENCES User(user_id)
);

CREATE TABLE RoomType (
    room_type_id INT PRIMARY KEY,
    type_name VARCHAR(20),
    description TEXT
);

CREATE TABLE StudySession (
    session_id INT PRIMARY KEY,
    course_offering_id INT,
    location_id INT,
    organizer_id INT,
    max_attendees INT CHECK (max_attendees > 0),
    description VARCHAR(200),
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    chill_level INT CHECK (chill_level BETWEEN 1 AND 5), #placeholder scale
    room_type_id INT NULL,
    FOREIGN KEY (course_offering_id) REFERENCES CourseOffering(course_offering_id),
    FOREIGN KEY (location_id) REFERENCES Location(location_id),
    FOREIGN KEY (organizer_id) REFERENCES User(user_id),
    FOREIGN KEY (room_type_id) REFERENCES RoomType(room_type_id)
);

CREATE TABLE Attendance (
    user_id INT,
    session_id INT,
    PRIMARY KEY (user_id, session_id),
    FOREIGN KEY (user_id) REFERENCES User(user_id),
    FOREIGN KEY (session_id) REFERENCES StudySession(session_id)
);

CREATE TABLE Tag (
    tag_id INT PRIMARY KEY,
    tag_name VARCHAR(50)
);

CREATE TABLE SessionTag (
    session_id INT,
    tag_id INT,
    PRIMARY KEY (session_id, tag_id),
    FOREIGN KEY (session_id) REFERENCES StudySession(session_id),
    FOREIGN KEY (tag_id) REFERENCES Tag(tag_id)
);

CREATE TABLE Resource (
    resource_id INT PRIMARY KEY,
    session_id INT,
    uploaded_by INT,
    resource_name VARCHAR(50),
    resource_url TEXT,
    FOREIGN KEY (session_id) REFERENCES StudySession(session_id),
    FOREIGN KEY (uploaded_by) REFERENCES User(user_id)
);

CREATE TABLE Reminder (
    reminder_id INT PRIMARY KEY,
    user_id INT,
    session_id INT,
    reminder_time TIMESTAMP,
    reminder_sent BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (user_id) REFERENCES User(user_id),
    FOREIGN KEY (session_id) REFERENCES StudySession(session_id)
);
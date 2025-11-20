
--------------------------------POPULATE DATA-------------------------------------------------

--INSERT INTO USER

INSERT INTO User (user_id, email, password_hash, first_name, last_name, phone, created_at)
VALUES (1, 'qo237@nyu.edu', 'b3d17ebbe4f2b75d27b6309cfaae1487b667301a73951e7d523a039cd2dfe110','quincy', 'oldland', 1111111111, NOW());
        
INSERT INTO User (user_id, email, password_hash, first_name, last_name, phone, created_at)
VALUES (2, 'wdc9645@nyu.edu', 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f','Will', 'Chanania', 2222222222, NOW());
    
INSERT INTO User (user_id, email, password_hash, first_name, last_name, phone, created_at)
VALUES (3, 'rmf9265@nyu.edu', 'b9c950640e1b3740e98acb93e669c65766f6670dd1609ba91ff41052ba48c6f3','Ryan', 'Fleishman', 3333333333, NOW());

INSERT INTO User (user_id, email, password_hash, first_name, last_name, phone, created_at)
VALUES(4, 'hk4469@nyu.edu', '3700adf1f25fab8202c1343c4b0b4e3fec706d57cad574086467b8b3ddf273ec','Hemanesh', 'Kamireddy', 4444444444, NOW());

INSERT INTO User (user_id, email, password_hash, first_name, last_name, phone, created_at)
VALUES (6, 'jls7821@nyu.edu', '9b74c9897bac770ffc029102a200c5de643f7d4b1f9a8b2c8f3b3b21fdd2d7a5', 'Julia', 'Stevens', 6666666666, NOW());

INSERT INTO User (user_id, email, password_hash, first_name, last_name, phone, created_at)
VALUES (7, 'tpn4912@nyu.edu', '6c569aabbf7775ef8fc570e228c16b981a5f68f7b0b5b0a9aefc98a54e8c2c6f', 'Tom', 'Nguyen', 7777777777, NOW());

INSERT INTO User (user_id, email, password_hash, first_name, last_name, phone, created_at)
VALUES (8, 'eba3156@nyu.edu', '2c9341ca4cf3d87b9e4e5a4f4d8a95f799ee8f6a6c8f77a6d29d1d79efc5b3f4', 'Ella', 'Barnes', 8888888888, NOW());

INSERT INTO User (user_id, email, password_hash, first_name, last_name, phone, created_at)
VALUES (9, 'mrt5127@nyu.edu', '7c6a180b36896a0a8c02787eeafb0e4c7c2e93c432f0e5b6c2f9a4b2f8f8bba9', 'Marcus', 'Trent', 9999999999, NOW());

INSERT INTO User (user_id, email, password_hash, first_name, last_name, phone, created_at)
VALUES (10, 'arl2380@nyu.edu', '3a7bd3e2360a3d80a9f23c0a8b1d8a1e8b7a47b56f833b5d3a1a10c4f7a5c5a2', 'Ava', 'Lorenzo', 1010101010, NOW());

INSERT INTO User (user_id, email, password_hash, first_name, last_name, phone, created_at)
VALUES (11, 'ncl3073@nyu.edu', '4f2a1d9b8c3e7f6a5b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2', 'Noah', 'Clark', 1112223333, NOW());

--INSERT INTO TAG
INSERT INTO tag (tag_id, tag_name)
VALUES 
(1, 'coding'),
(2, 'lab'),
(3, 'homework'),
(4, 'exam prep'),
(5, 'lecture notes'),
(6, 'project'),
(7, 'research'),
(8, 'group work'),
(9, 'presentation'),
(10, 'final review');

--INSERT INTO LOCATION

INSERT INTO Location (location_id, address, room_number, created_by_user)
VALUES 
(1, 'Main Library', '101', 1),
(2, 'Main Library', '102', 2),
(3, 'Main Library', 'Study Room A', 3),
(4, 'Student Center', '201', 4),
(5, 'Engineering Building', '305', 2),
(6, 'Science Center', 'Lab 1', 6),
(7, 'Innovation Hub', '2nd Floor Commons', 7),
(8, 'Online', 'Zoom 998-221-447', 8),
(9, 'Business School', 'Room 410', 9),
(10, 'Art Building', 'Studio 5', 10);

--INSERT INTO COURSE OFFERING 

INSERT INTO CourseOffering
(course_offering_id, title, section, year, term, created_by_user)
VALUES
(1, 'Principles Of Database Systems', 'A', 2025, 1, 2),
(2, 'Coding 101', 'B', 2025, 2, 3),
(3, 'Data Structures', 'A', 2025, 1, 4),
(4, 'Algorithms', 'C', 2025, 3, 6),
(5, 'Web Development', 'A', 2024, 1, 7),
(6, 'Machine Learning', 'B', 2025, 2, 8),
(7, 'Linear Algebra', 'D', 2023, 4, 9),
(8, 'Operating Systems', 'A', 2025, 2, 10),
(9, 'Computer Networks', 'B', 2025, 3, 11),
(10, 'Software Engineering', 'C', 2024, 2, 2);

--INSERT INTO ROOMTYPE

INSERT INTO RoomType (room_type_id, type_name, description)
VALUES
(1, 'Quiet Study Room', 'Small space for individual study or silent focus.'),
(2, 'Collaborative Commons', 'Open area suited for group collaboration and discussion.'),
(3, 'Computer Lab', 'Room with desktop stations and whiteboards for coding practice.'),
(4, 'Lecture Hall', 'Large space with tiered seating, designed for lectures or presentations.'),
(5, 'Seminar Room', 'Medium-sized room for small classes or group discussions.'),
(6, 'Workshop Room', 'Hands-on learning space equipped with tools and materials.'),
(7, 'Innovation Hub', 'Modern, tech-enabled area for brainstorming and project development.'),
(8, 'Art Studio', 'Creative space equipped for art and design work.'),
(9, 'Meeting Room', 'Room equipped for meetings, tutoring, or faculty office hours.'),
(10, 'Virtual Room', 'Online session space designated for remote collaboration.');

--INSERT INTO STUDY SESSION

INSERT INTO StudySession 
(session_id, course_offering_id, location_id, organizer_id, max_attendees, description, start_time, end_time, chill_level, room_type_id)
VALUES
(3, 3, 1, 2, 25, 'Dynamic programming drill session with whiteboard practice.', '2025-02-22 07:00:00', '2025-02-22 09:30:00', 3, 1),
(4, 4, 5, 3, 18, 'Greedy vs. divide-and-conquer problem showdown.', '2025-02-23 15:00:00', '2025-02-23 17:00:00', 2, 2),
(5, 5, 4, 4, 15, 'Pair programming on responsive layout challenges.', '2025-02-24 17:00:00', '2025-02-24 19:00:00', 1, 2),
(6, 1, 2, 6, 25, 'Principles Of Database Systems - early morning prep.', '2025-02-21 06:00:00', '2025-02-21 08:00:00', 1, 1),
(7, 7, 3, 7, 12, 'Eigenvalues concept review with curated problem walkthroughs.', '2025-02-25 13:30:00', '2025-02-25 15:00:00', 2, 3),
(8, 2, 1, 8, 40, 'Hands-on debugging lab. Bring a failing script!', '2025-02-22 10:00:00', '2025-02-22 12:00:00', 1, 1),
(9, 6, 7, 9, 16, 'AutoML demo session featuring new tooling.', '2025-02-26 16:00:00', '2025-02-26 17:30:00', 1, 2),
(10, 3, 6, 2, 18, 'Lab computers reserved; arrive 10 minutes early.', '2025-02-27 11:00:00', '2025-02-27 13:00:00', 3, 3),
(11, 8, 9, 10, 20, 'OS process scheduling walkthrough with hands-on examples.', '2025-03-01 14:00:00', '2025-03-01 16:00:00', 2, 4),
(12, 9, 10, 11, 25, 'Intro to computer networking with routing simulations.', '2025-03-02 13:00:00', '2025-03-02 15:00:00', 1, 5);

--INSERT INTO REMINDER

INSERT INTO Reminder
(reminder_id, session_id, user_id, reminder_time, reminder_sent)
VALUES
(1, 11, 1, '2025-12-01 13:00:00', 0), 
(2, 3, 4,  '2025-11-20 19:00:00', 1),
(3, 4, 2,  '2025-11-21 14:00:00', 0),
(4, 5, 3,  '2025-11-22 16:00:00', 0),
(5, 6, 6,  '2025-11-23 05:00:00', 1),
(6, 7, 7,  '2025-11-24 12:30:00', 0),
(7, 8, 8,  '2025-11-25 09:00:00', 0),
(8, 9, 9,  '2025-11-26 15:00:00', 1),
(9, 10, 10,'2025-11-27 10:00:00', 0),
(10, 12, 11,'2025-11-02 12:00:00', 0);

--INSERT INTO RESOURCE

INSERT INTO Resource
(resource_id, session_id, uploaded_by, resource_name, resource_url)
VALUES
(1, 7, 1, 'ER Modeling Worksheet', 'https://cdn.example.com/resources/er-modeling.pdf'),
(2, 4, 2, 'Greedy vs Divide Notes', 'https://cdn.example.com/resources/greedy-notes.pdf'),
(3, 3, 4, 'Dynamic Programming Practice Set', 'https://cdn.example.com/resources/dp-practice.pdf'),
(4, 5, 3, 'Web Layout Flexbox Guide', 'https://cdn.example.com/resources/flexbox-guide.pdf'),
(5, 6, 6, 'Database Lecture Slides', 'https://cdn.example.com/resources/db-lecture-slides.pdf'),
(6, 7, 7, 'Eigenvalue Review Notes', 'https://cdn.example.com/resources/eigenvalues-review.pdf'),
(7, 8, 8, 'Debugging Workshop Files', 'https://cdn.example.com/resources/debugging-files.zip'),
(8, 9, 9, 'Machine Learning Tools Demo', 'https://cdn.example.com/resources/ml-tools-demo.pdf'),
(9, 10, 10, 'Data Structures Lab Reference', 'https://cdn.example.com/resources/data-structures-lab.pdf'),
(10, 12, 11, 'Networking Routing Simulation', 'https://cdn.example.com/resources/networking-routing-sim.pdf');

--INSERT INTO ATTENDANCE

INSERT INTO Attendance (user_id, session_id)
VALUES
(2, 3),
(3, 3),
(4, 3),
(2, 4),
(1, 4),
(6, 5),
(7, 6),
(8, 6),
(9, 7),
(10, 8);

--INSERT INTO SESSION TAG

INSERT INTO SessionTag (session_id, tag_id)
VALUES
(3, 1),
(3, 4),
(4, 2),
(5, 1),
(6, 4),
(7, 2),
(8, 3),
(9, 1),
(9, 2),
(10, 2);


-------------------------------RETRIEVE DATA---------------------------------------

--FIND A USERS SESSION

SELECT *
FROM StudySession s
INNER JOIN Attendance a
ON s.session_id = a.session_id
WHERE a.user_id = 1

SELECT *
FROM StudySession s
INNER JOIN Attendance a
ON s.session_id = a.session_id
WHERE a.user_id = 2

--LOGIN/VERIFY A USER

SELECT user_id, password_hash
FROM User
WHERE email = 'qo237@nyu.edu'

SELECT user_id, password_hash
FROM User
WHERE email = 'wdc9645@nyu.edu'

--GET A USER's PROFILE

SELECT * FROM User where user_id = 4

SELECT * FROM User where user_id = 7

--SHOW COURSE OFFERINGS 

SELECT title, section FROM CourseOffering

--LIST LOCATIONS 

SELECT name, room_number FROM Location

--LIST ROOMTYPES

SELECT type_name, description FROM RoomType

--LIST TAGS

SELECT tag_name FROM Tag

--SELECT SESSIONS WITH FILTERS

SELECT * 
FROM StudySession s
INNER JOIN Location l
ON s.location_id = l.location_id
WHERE l.address LIKE 'Main Library'

SELECT * 
FROM StudySession s
INNER JOIN Location l
ON s.location_id = l.location_id
WHERE l.address LIKE 'Main Library'
AND s.max_attendees < 15

--LIST RESOURCES FOR SESSION

SELECT * 
FROM Resource r
INNER JOIN StudySession s 
ON r.session_id = s.session_id
WHERE s.session_id = 5

--------------------------------UPDATE DATA-------------------------------------------

--UPDATE USER INFO 

UPDATE User 
SET phone = 1231231234
WHERE User.user_id = 1

UPDATE User 
SET email = 'bob@gmail.com'
WHERE User.user_id = 8

--UPDATE COURSE INFO 

UPDATE CourseOffering 
SET section = 'B' 
WHERE course_offering_id = 3


--UPDATE SESSION DETAILS 

UPDATE StudySession
SET max_attendees = 5, location_id = 6
WHERE session_id = 6


--MARK REMINDER AS SENT 

UPDATE Reminder 
SET reminder_sent = 1
WHERE reminder_id = 4

--UPDATE LOCATION INFO 

UPDATE Location
SET room_number = 505
WHERE location_id = 7


----------------------------------CREATE DATA-----------------------------------------

--INSERT AN ATTENDANCE RECORD 

INSERT INTO Attendance (user_id, session_id)
VALUES (1, 5)

INSERT INTO Attendance (user_id, session_id)
VALUES (4, 7)

--REGISTER A NEW USER 

INSERT INTO User (user_id, email, password_hash, first_name, last_name, phone, created_at)
VALUES 
(12, 'newuser@nyu.edu', 'a1b2c3d4e5f60718293a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5', 'Jordan', 'Miles', 1234567890, NOW());

--CREATE A NEW COURSE OFFERING 

INSERT INTO CourseOffering
(course_offering_id, title, section, year, term, created_by_user)
VALUES
(11, 'Artificial Intelligence Fundamentals', 'A', 2025, 3, 12);

--CREATE A NEW LOCATION

INSERT INTO Location 
(location_id, address, room_number, created_by_user)
VALUES
(11, 'Business Innovation Center', 'Room 210', 12);

--CREATE A NEW ROOMTYPE

INSERT INTO RoomType
(room_type_id, type_name, description)
VALUES
(11, 'Conference Room', 'Professional space equipped with presentation screens, whiteboards, and seating for team discussions or workshops.');

--CREATE A NEW TAG

INSERT INTO Tag (tag_id, tag_name)
VALUES
(11, 'final exam prep');

--CREATE A NEW SESSION TAG

INSERT INTO SessionTag (session_id, tag_id)
VALUES
(10, 11);

--CREATE A NEW REMINDER

INSERT INTO Reminder
(reminder_id, session_id, user_id, reminder_time, reminder_sent)
VALUES
(11, 11, 10, '2025-03-01 13:00:00', 0);

--CREATE A NEW RESOURCE
INSERT INTO Resource
(resource_id, session_id, uploaded_by, resource_name, resource_url)
VALUES
(11, 11, 12, 'AI Fundamentals Lecture Slides', 'https://cdn.example.com/resources/ai-fundamentals-slides.pdf');

------------------------------------------DELETES------------------------------------------

--LEAVE A SESSION 

DELETE FROM Attendance
WHERE user_id = 2

DELETE FROM Attendance
WHERE user_id = 7

--DELETE A RESOURCE

DELETE FROM Resource
WHERE resource_id = 7


---------------------------------------ADVANCED SQL--------------------------------------------

--WHEN A USER LEAVES A SESSION (AKA AN ATTENDANCE IS DELETED) DELETE THE CORRESPONDING REMINDER
DELIMITER $$

CREATE TRIGGER delete_reminder_after_attendance
AFTER DELETE ON Attendance
FOR EACH ROW
BEGIN
    DELETE FROM Reminder
    WHERE user_id = OLD.user_id
      AND session_id = OLD.session_id;
END$$

DELIMITER ;

--CHECK HOW MANY SEATS REMAIN IN A GIVEN SESSION
DELIMITER $$

CREATE FUNCTION seats_remaining(p_session_id INT)
RETURNS INT
DETERMINISTIC
BEGIN
  DECLARE total INT;
  DECLARE max_cap INT;

  SELECT COUNT(*) INTO total FROM Attendance WHERE session_id = p_session_id;
  SELECT max_attendees INTO max_cap FROM StudySession WHERE session_id = p_session_id;

  RETURN (max_cap - total);
END$$

DELIMITER ;

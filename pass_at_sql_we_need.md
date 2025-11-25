*users and accounts*  
-- register new user (INSERT INTO User ...)  
-- Login/verify (SELECT user_id, password FROM User WHERE email = ...)  
-- get user's profile (SELECT * FROM User where user_id = ..)  
-- update info (UPDATE User SET ... WHERE user_id = ...)  
-- Delete account (DELETE FROM user WHERE user_id ...)  
  
*Course Offerings*  
-- new course offering (INSERT INTO CourseOffering ...)  
-- showing course offerings (SELECT title, section (maybe just *) FROM CourseOffering)   
-- update course info (UPDATE CourseOffering SET ... WHERE course_offering_id = ...)  
-- delete course offering (DELETE FROM CourseOffering course_offering_id = ...)  

*Locations*  
-- new location (INSERT INTO Location ...)  
-- list locations (SELECT name (maybe just *) FROM Location)  
-- update (UPDATE Location SET ... WHERE location_id = ...)  

*Room Type*  
-- add new (INSERT INTO RoomType ...)  
-- list room types (SELECT name FROM RoomType)  
  
*Tags*  
-- add new tag (INSERT INTO)  
-- list tags (SELECT tag_name FROM Tag)  
-- add a tag for a session (INSERT INTO SessionTag (session_id, tag_id) VALUES (session, tag)  
-- remove a tag for a session (Delete From SessionTag WHERE session id = this and tag_id = target)  

*Resources*    
-- add resource (INSERT INTO Resource)  
-- list resources for session (SELECT * FROM Resource WHERE session_id = ...)  
-- delete resource (DELETE yada yada)  

*Reminders*  
-- sorry I got too bored at this point it's the usual shit  
  
*Study Sessions*  
-- create session (INSERT INTO StudySession ...)  
-- List all upcoming sessions  
-- Filter by course/location/tag/year/term/professor  
-- not in ui but we should have ability to see own sessions  
-- get all session details (lotta joins in this)  
-- Update session info  
-- delete session  

*attendence*  
-- join sess (insert)  
-- leave ssess (delete)  
-- list attendees  




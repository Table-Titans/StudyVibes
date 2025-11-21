from sqlalchemy import text

find_course_query = text("""
    SELECT 
        course_offering_id AS id,
        title,
        section,
        year,
        term,
        professor_name
    FROM CourseOffering
    WHERE course_offering_id = :course_id
    LIMIT 1
""")

find_location_query = text("""
    SELECT 
        location_id AS id,
        address,
        room_number
    FROM Location
    WHERE location_id = :location_id
    LIMIT 1
""")

find_session_query = text("""
    SELECT 
        s.session_id,
        s.course_offering_id,
        s.location_id,
        s.organizer_id,
        s.max_attendees,
        s.description,
        s.start_time,
        s.end_time,
        s.chill_level,
        s.room_type_id,
        c.title as course_title,
        c.section as course_section,
        l.address as location_address,
        l.room_number as location_room
    FROM StudySession s
    LEFT JOIN CourseOffering c ON s.course_offering_id = c.course_offering_id
    LEFT JOIN Location l ON s.location_id = l.location_id
    WHERE s.session_id = :session_id
    LIMIT 1
""")

find_room_type_query = text("""
    SELECT 
        room_type_id AS id,
        type_name,
        description
    FROM RoomType
    WHERE room_type_id = :room_type_id
    LIMIT 1
""")

get_session_tag_ids_query = text("""
    SELECT tag_id
    FROM SessionTag
    WHERE session_id = :session_id
""")

find_tag_by_id_query = text("""
    SELECT tag_id AS id, tag_name
    FROM Tag
    WHERE tag_id = :tag_id
    LIMIT 1
""")

get_resources_for_session_query = text("""
    SELECT 
        resource_id AS id,
        session_id,
        resource_name,
        resource_url,
        uploaded_by
    FROM Resource
    WHERE session_id = :session_id
""")

get_reminders_for_session_query = text("""
    SELECT 
        reminder_id AS id,
        session_id,
        user_id,
        reminder_time,
        reminder_sent
    FROM Reminder
    WHERE session_id = :session_id
""")

fetch_all_courses_query = text("""
    SELECT 
        course_offering_id AS id,
        title,
        section,
        year,
        term,
        professor_name
    FROM CourseOffering
""")

fetch_all_attendees_query = text("""
    SELECT 
        first_name, 
        LEFT(last_name, 1) AS last_init 
    FROM User U 
    JOIN Attendance A ON U.user_id = A.user_id
    JOIN StudySession S ON S.session_id = A.session_id
    WHERE S.session_id = :session_id
""")

fetch_all_locations_query = text("""
    SELECT 
        location_id AS id,
        address,
        room_number
    FROM Location
""")

fetch_all_room_types_query = text("""
    SELECT 
        room_type_id AS id,
        type_name,
        description
    FROM RoomType
""")

fetch_all_tags_query = text("""
    SELECT 
        tag_id AS id,
        tag_name
    FROM Tag
""")

list_all_sessions_query = text("""
    SELECT 
        s.session_id,
        s.course_offering_id,
        s.location_id,
        s.organizer_id,
        s.max_attendees,
        s.description,
        s.start_time,
        s.end_time,
        s.chill_level,
        s.room_type_id,
        c.title AS course_title,
        c.section AS course_section,
        l.address AS location_address,
        l.room_number AS location_room,
        COUNT(a.user_id) AS attendance_count
    FROM StudySession s
    INNER JOIN CourseOffering c 
        ON s.course_offering_id = c.course_offering_id
    INNER JOIN Location l 
        ON s.location_id = l.location_id
    LEFT JOIN Attendance a 
        ON a.session_id = s.session_id
    GROUP BY 
        s.session_id,
        s.course_offering_id,
        s.location_id,
        s.organizer_id,
        s.max_attendees,
        s.description,
        s.start_time,
        s.end_time,
        s.chill_level,
        s.room_type_id,
        c.title,
        c.section,
        l.address,
        l.room_number
    ORDER BY s.start_time DESC;
""")

user_sessions_query = text("""
        (
        SELECT 
            s.session_id,
            s.course_offering_id,
            s.location_id,
            s.organizer_id,
            s.max_attendees,
            s.description,
            s.start_time,
            s.end_time,
            s.chill_level,
            s.room_type_id,
            c.title  AS course_title,
            c.section AS course_section,
            l.address AS location_address,
            l.room_number AS location_room,
            COALESCE(ac.attendance_count, 0) AS attendance_count
        FROM StudySession s
        INNER JOIN Attendance a ON s.session_id = a.session_id
        LEFT  JOIN CourseOffering c ON s.course_offering_id = c.course_offering_id
        LEFT  JOIN Location l ON s.location_id = l.location_id
        LEFT  JOIN (
            SELECT session_id, COUNT(*) AS attendance_count
            FROM Attendance
            GROUP BY session_id
        ) ac ON ac.session_id = s.session_id
        WHERE a.user_id = :id
    )
    UNION
    (
        SELECT 
            s.session_id,
            s.course_offering_id,
            s.location_id,
            s.organizer_id,
            s.max_attendees,
            s.description,
            s.start_time,
            s.end_time,
            s.chill_level,
            s.room_type_id,
            c.title  AS course_title,
            c.section AS course_section,
            l.address AS location_address,
            l.room_number AS location_room,
            COALESCE(ac.attendance_count, 0) AS attendance_count
        FROM StudySession s
        LEFT JOIN CourseOffering c ON s.course_offering_id = c.course_offering_id
        LEFT JOIN Location l       ON s.location_id = l.location_id
        LEFT JOIN (
            SELECT session_id, COUNT(*) AS attendance_count
            FROM Attendance
            GROUP BY session_id
        ) ac ON ac.session_id = s.session_id
        WHERE s.organizer_id = :id
    )
    ORDER BY start_time DESC;

""")

login_lookup_query = text("""
    SELECT user_id, email, password_hash, first_name, last_name, phone
    FROM User
    WHERE LOWER(email) = :email
    LIMIT 1
""")

register_email_duplicate_query = text("""
    SELECT user_id
    FROM User
    WHERE LOWER(email) = :email
    LIMIT 1
""")

register_insert_user_query = text("""
    INSERT INTO User (email, password_hash, first_name, last_name, phone, created_at)
    VALUES (:email, :password_hash, :first_name, :last_name, :phone, NOW())
""")

find_user_by_email_desc_query = text("""
    SELECT user_id
    FROM User
    WHERE LOWER(email) = :email
    ORDER BY user_id DESC
    LIMIT 1
""")

fetch_user_by_id_query = text("""
    SELECT user_id, email, password_hash, first_name, last_name, phone
    FROM User
    WHERE user_id = :user_id
    LIMIT 1
""")

insert_study_session_query = text("""
    INSERT INTO StudySession (
        course_offering_id,
        location_id,
        organizer_id,
        max_attendees,
        description,
        start_time,
        end_time,
        chill_level,
        room_type_id
    )
    VALUES (
        :course_offering_id,
        :location_id,
        :organizer_id,
        :max_attendees,
        :description,
        :start_time,
        :end_time,
        :chill_level,
        :room_type_id
    )
""")

latest_session_id_query = text("""
    SELECT session_id
    FROM StudySession
    ORDER BY session_id DESC
    LIMIT 1
""")

insert_attendance_query = text("""
    INSERT INTO Attendance (user_id, session_id)
    VALUES (:user_id, :session_id)
""")

insert_resource_query = text("""
    INSERT INTO Resource (session_id, uploaded_by, resource_name, resource_url)
    VALUES (:session_id, :uploaded_by, :resource_name, :resource_url)
""")

insert_reminder_query = text("""
    INSERT INTO Reminder (session_id, user_id, reminder_time, reminder_sent)
    VALUES (:session_id, :user_id, :reminder_time, 0)
""")

insert_session_tag_query = text("""
    INSERT INTO SessionTag (session_id, tag_id)
    VALUES (:session_id, :tag_id)
""")

view_session_query = text("""
    SELECT 
        s.session_id,
        s.course_offering_id,
        s.location_id,
        s.organizer_id,
        s.max_attendees,
        s.description,
        s.start_time,
        s.end_time,
        s.chill_level,
        s.room_type_id,
        c.title as course_title,
        c.section as course_section,
        c.year as course_year,
        c.term as course_term,
        l.address as location_address,
        l.room_number as location_room
    FROM StudySession s
    LEFT JOIN CourseOffering c ON s.course_offering_id = c.course_offering_id
    LEFT JOIN Location l ON s.location_id = l.location_id
    WHERE s.session_id = :session_id
""")

session_exists_query = text("""
    SELECT session_id
    FROM StudySession
    WHERE session_id = :session_id
    LIMIT 1
""")

attendance_exists_query = text("""
    SELECT user_id
    FROM Attendance
    WHERE session_id = :session_id AND user_id = :user_id
    LIMIT 1
""")

delete_attendance_query = text("""
    DELETE FROM Attendance
    WHERE session_id = :session_id AND user_id = :user_id
""")

update_session_query = text("""
    UPDATE StudySession
    SET course_offering_id = :course_id,
        location_id = :location_id,
        max_attendees = :max_attendees,
        description = :description,
        start_time = :start_time,
        end_time = :end_time,
        chill_level = :chill_level,
        room_type_id = :room_type_id
    WHERE session_id = :session_id
""")

delete_session_attendance_query = text("""
    DELETE FROM Attendance
    WHERE session_id = :session_id
""")

delete_session_tags_query = text("""
    DELETE FROM SessionTag
    WHERE session_id = :session_id
""")

delete_session_query = text("""
    DELETE FROM StudySession
    WHERE session_id = :session_id
""")

search_locations_query = text("""
    SELECT 
        location_id AS id,
        address,
        room_number
    FROM Location
    WHERE LOWER(address) LIKE :pattern
    OR LOWER(room_number) LIKE :pattern
    ORDER BY address
    LIMIT 25
""")

list_locations_query = text("""
    SELECT 
        location_id AS id,
        address,
        room_number
    FROM Location
    ORDER BY address
    LIMIT 25
""")

location_duplicate_query = text("""
    SELECT location_id
    FROM Location
    WHERE LOWER(address) = :address
    AND LOWER(room_number) = :room
    LIMIT 1
""")

latest_location_id_query = text("""
    SELECT location_id
    FROM Location
    ORDER BY location_id DESC
    LIMIT 1
""")

insert_location_query = text("""
    INSERT INTO Location (address, room_number, created_by_user)
    VALUES (:address, :room_number, :created_by_user)
""")

search_courses_query = text("""
    SELECT 
        course_offering_id AS id,
        title,
        section,
        year,
        term,
        professor_name
    FROM CourseOffering
    WHERE LOWER(title) LIKE :pattern
    OR LOWER(section) LIKE :pattern
    OR LOWER(professor_name) LIKE :pattern
    ORDER BY title
    LIMIT 25
""")

list_courses_query = text("""
    SELECT 
        course_offering_id AS id,
        title,
        section,
        year,
        term,
        professor_name
    FROM CourseOffering
    ORDER BY title
    LIMIT 25
""")

course_duplicate_query = text("""
    SELECT course_offering_id
    FROM CourseOffering
    WHERE LOWER(title) = :title
    AND LOWER(section) = :section
    AND year = :year
    AND term = :term
    LIMIT 1
""")

insert_course_offering_query = text("""
    INSERT INTO CourseOffering (title, section, year, term, professor_name, created_by_user)
    VALUES (:title, :section, :year, :term, :professor_name, :created_by_user)
""")

latest_course_id_query = text("""
    SELECT course_offering_id
    FROM CourseOffering
    ORDER BY course_offering_id DESC
    LIMIT 1
""")

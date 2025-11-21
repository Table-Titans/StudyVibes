from datetime import datetime

from flask import render_template, request, redirect, url_for, flash, jsonify, abort, current_app
from flask_login import (
    current_user,
    login_required,
    login_user,
    logout_user,
)
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from models import User
import sql_queries as queries


def register_routes(app, db):

    def find_course(course_id):
        if not course_id:
            return None
        row = db.session.execute(
            queries.find_course_query, {"course_id": course_id}
        ).first()
        return dict(row._mapping) if row else None

    def find_location(location_id):
        if not location_id:
            return None
        row = db.session.execute(
            queries.find_location_query, {"location_id": location_id}
        ).first()
        return dict(row._mapping) if row else None

    def find_session(session_id):
        if not session_id:
            return None
        row = db.session.execute(
            queries.find_session_query, {"session_id": session_id}
        ).first()
        if not row:
            return None
        session_dict = {
            "id": row.session_id,
            "session_id": row.session_id,
            "course_id": row.course_offering_id,
            "location_id": row.location_id,
            "organizer_id": row.organizer_id,
            "max_attendees": row.max_attendees,
            "description": row.description,
            "start_time": row.start_time.isoformat() if row.start_time else None,
            "end_time": row.end_time.isoformat() if row.end_time else None,
            "chill_level": row.chill_level,
            "room_type_id": row.room_type_id,
            "title": row.course_title or row.description or "Study Session",
            "location": f"{row.location_address} - Room {row.location_room}" if row.location_address else "TBD",
            "time": row.start_time.strftime('%b %d, %I:%M %p') if row.start_time else "TBD",
            "attendees": "TBD",
        }
        return session_dict

    def find_room_type(room_type_id):
        if not room_type_id:
            return None
        row = db.session.execute(
            queries.find_room_type_query, {"room_type_id": room_type_id}
        ).first()
        return dict(row._mapping) if row else None

    def get_session_tag_ids(session_id):
        if not session_id:
            return []
        rows = db.session.execute(
            queries.get_session_tag_ids_query, {"session_id": session_id}
        ).fetchall()
        return [row.tag_id for row in rows]

    def find_tags(tag_ids):
        if not tag_ids:
            return []
        tags = []
        for tag_id in tag_ids:
            row = db.session.execute(
                queries.find_tag_by_id_query,
                {"tag_id": tag_id},
            ).first()
            if row:
                tags.append(dict(row._mapping))
        return tags

    def get_resources_for_session(session_id):
        rows = db.session.execute(
            queries.get_resources_for_session_query,
            {"session_id": session_id},
        ).fetchall()
        return [dict(row._mapping) for row in rows]

    def get_reminders_for_session(session_id):
        rows = db.session.execute(
            queries.get_reminders_for_session_query,
            {"session_id": session_id},
        ).fetchall()
        reminders = []
        for row in rows:
            reminder_copy = dict(row._mapping)
            reminder_copy['display_time'] = format_datetime_string(reminder_copy.get('reminder_time'))
            reminders.append(reminder_copy)
        return reminders

    def format_datetime_string(value):
        if not value:
            return None
        if isinstance(value, datetime):
            dt = value
        else:
            try:
                dt = datetime.fromisoformat(value)
            except ValueError:
                return value
        formatted = dt.strftime("%B %d, %Y %I:%M %p")
        return formatted.replace(" 0", " ").lstrip("0")

    def fetch_all_courses():
        rows = db.session.execute(queries.fetch_all_courses_query).fetchall()
        return [dict(row._mapping) for row in rows]

    def fetch_all_locations():
        rows = db.session.execute(queries.fetch_all_locations_query).fetchall()
        return [dict(row._mapping) for row in rows]

    def fetch_all_room_types():
        rows = db.session.execute(queries.fetch_all_room_types_query).fetchall()
        return [dict(row._mapping) for row in rows]

    def fetch_all_tags():
        rows = db.session.execute(queries.fetch_all_tags_query).fetchall()
        return [dict(row._mapping) for row in rows]

    def build_session_context(session_record):
        if not session_record:
            return None

        session_copy = dict(session_record)
        course = find_course(session_copy.get("course_id"))
        location = find_location(session_copy.get("location_id"))

        # Prefer explicit start/end times; fall back to generic time if needed
        start_display = session_copy.get("start_time")
        end_display = session_copy.get("end_time")
        if start_display and "T" in start_display:
            start_display = format_datetime_string(start_display)
        if end_display and "T" in end_display:
            end_display = format_datetime_string(end_display)

        if not start_display:
            start_display = session_copy.get("time") or "TBD"
        if not end_display:
            end_display = session_copy.get("end_time_display") or "TBD"

        session_copy["start_time"] = start_display
        session_copy["end_time"] = end_display

        attendees_data = session_copy.get(
            "attendee_list", session_copy.get("attendees")
        )
        room_type = find_room_type(session_copy.get("room_type_id"))
        session_copy["room_type"] = room_type

        tag_ids = session_copy.get("tag_ids") or get_session_tag_ids(session_copy["id"])
        session_copy["tag_ids"] = tag_ids
        session_copy["tags"] = find_tags(tag_ids)
        session_copy["resources"] = get_resources_for_session(session_copy["id"])
        session_copy["reminders"] = get_reminders_for_session(session_copy["id"])

        return {
            "session": session_copy,
            "course": course,
            "location": location,
            "attendees": attendees_data,
        }

    @app.route("/")
    @login_required
    def home():
        result = db.session.execute(queries.list_all_sessions_query)
        rows = result.fetchall()
        all_sessions = []

        for row in rows:
            session_dict = {
                'id': row.session_id,
                'session_id': row.session_id,
                'course_id': row.course_offering_id,
                'location_id': row.location_id,
                'organizer_id': row.organizer_id,
                'max_attendees': row.max_attendees,
                'description': row.description,
                'start_time': row.start_time.isoformat() if row.start_time else None,
                'end_time': row.end_time.isoformat() if row.end_time else None,
                'chill_level': row.chill_level,
                'room_type_id': row.room_type_id,
                'title': row.course_title or row.description or 'Study Session',
                'location': f"{row.location_address} - Room {row.location_room}" if row.location_address else 'TBD',
                'time': row.start_time.strftime('%b %d, %I:%M %p') if row.start_time else 'TBD',
                'attendees': row.attendance_count,
                'is_organizer': row.organizer_id == current_user.user_id,
            }
            all_sessions.append(session_dict)
        rows = db.session.execute(
            queries.user_sessions_query,
            {"id": current_user.user_id},
        ).fetchall()
        my_sessions = []
        for row in rows:
            session_dict = {
                'id': row.session_id,
                'session_id': row.session_id,
                'course_id': row.course_offering_id,
                'location_id': row.location_id,
                'organizer_id': row.organizer_id,
                'max_attendees': row.max_attendees,
                'description': row.description,
                'start_time': row.start_time.isoformat() if row.start_time else None,
                'end_time': row.end_time.isoformat() if row.end_time else None,
                'chill_level': row.chill_level,
                'room_type_id': row.room_type_id,
                'title': row.course_title or row.description or 'Study Session',
                'location': f"{row.location_address} - Room {row.location_room}" if row.location_address else 'TBD',
                'time': row.start_time.strftime('%b %d, %I:%M %p') if row.start_time else 'TBD',
                'attendees': row.attendance_count,
                'is_organizer': row.organizer_id == current_user.user_id,  # Add this line

            }
            my_sessions.append(session_dict)

        return render_template("main_dashboard.html", 
                             my_sessions=my_sessions, 
                             join_sessions=all_sessions,
                             courses=fetch_all_courses(),
                             locations=fetch_all_locations(),
                             room_types=fetch_all_room_types(),
                             tags=fetch_all_tags())
    
    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            email = (request.form.get("email") or "").strip().lower()
            password = request.form.get("password") or ""

            if not email or not password:
                flash("Email and password are required.", "error")
                return redirect(url_for("login"))

            result = db.session.execute(
                queries.login_lookup_query, {"email": email}
            ).first()
            if not result:
                flash("Invalid email or password.", "error")
                return redirect(url_for("login"))

            user = User.from_record(result)
            if not user.password_hash or not check_password_hash(user.password_hash, password):
                flash("Invalid email or password.", "error")
                return redirect(url_for("login"))

            login_user(user)
            return redirect(url_for("home"))

        return render_template("auth/login.html", title="Login")

    @app.route("/register", methods=["GET", "POST"])
    def register():
        if request.method == "POST":
            first_name = (request.form.get("first_name") or "").strip()
            last_name = (request.form.get("last_name") or "").strip()
            email = (request.form.get("email") or "").strip().lower()
            phone = (request.form.get("phone") or "").strip()
            password = request.form.get("password") or ""
            confirm_password = request.form.get("confirm_password") or ""

            if not all([first_name, last_name, email, phone, password]):
                flash("All fields are required.", "error")
                return redirect(url_for("register"))

            if password != confirm_password:
                flash("Passwords do not match.", "error")
                return redirect(url_for("register"))

            duplicate = db.session.execute(
                queries.register_email_duplicate_query, {"email": email}
            ).first()
            if duplicate:
                flash("An account with that email already exists.", "error")
                return redirect(url_for("register"))

            password_hash = generate_password_hash(password)
            try:
                result = db.session.execute(
                    queries.register_insert_user_query,
                    {
                        "email": email,
                        "password_hash": password_hash,
                        "first_name": first_name,
                        "last_name": last_name,
                        "phone": phone,
                    },
                )
                db.session.commit()
            except Exception as exc:
                db.session.rollback()
                current_app.logger.exception("Registration insert failed")
                flash("Unable to create your account. Please try again.", "error")
                return redirect(url_for("register"))

            new_user_id = result.lastrowid
            if not new_user_id:
                new_user_id = db.session.execute(
                    queries.find_user_by_email_desc_query,
                    {"email": email},
                ).scalar()

            created_row = db.session.execute(
                queries.fetch_user_by_id_query, {"user_id": new_user_id}
            ).first()
            user = User.from_record(created_row)
            login_user(user)
            return redirect(url_for("home"))

        return render_template("auth/register.html", title="Register")

    @app.route("/logout")
    @login_required
    def logout():
        logout_user()
        return redirect(url_for("login"))

    @app.route("/create_session", methods=["GET", "POST"])
    @login_required
    def create_session():
        if request.method == "POST":
            course_id = request.form.get('course_id', type=int)
            location_id = request.form.get('location_id', type=int)
            max_attendees = request.form.get('max_attendees', type=int)
            description = request.form.get('description')
            start_time = request.form.get('start_time')
            end_time = request.form.get('end_time')
            chill_level = request.form.get('chill_level', type=int)
            room_type_id = request.form.get('room_type_id', type=int)
            reminder_time = request.form.get('reminder_time')
            tag_ids = []
            for raw_tag in request.form.getlist('tags'):
                try:
                    tag_ids.append(int(raw_tag))
                except (TypeError, ValueError):
                    continue
            resource_file = request.files.get('resource_file')

            if not course_id or not location_id:
                flash('Please pick a course and location from the list.', 'error')
                return redirect(request.url)

            if not max_attendees or not description or not start_time or not end_time or not chill_level or not room_type_id:
                flash('All required fields must be filled out.', 'error')
                return redirect(request.url)

            if resource_file and resource_file.filename:
                filename = secure_filename(resource_file.filename)
                if '.' not in filename:
                    flash('Resources must have a .txt or .pdf extension.', 'error')
                    return redirect(request.url)
                extension = filename.rsplit('.', 1)[-1].lower()
                if extension not in ('txt', 'pdf'):
                    flash('Resources must be a text or PDF file.', 'error')
                    return redirect(request.url)
                resource_name = filename
                resource_url = f"https://cdn.example.com/uploads/{filename}"
            else:
                resource_name = None
                resource_url = None

            selected_course = find_course(course_id)
            selected_location = find_location(location_id)
            room_type = find_room_type(room_type_id)

            if not selected_course or not selected_location or not room_type:
                flash('Could not find the selected course, location, or room type.', 'error')
                return redirect(request.url)

            start_value = start_time.replace("T", " ")
            end_value = end_time.replace("T", " ")

            session_result = db.session.execute(
                queries.insert_study_session_query,
                {
                    "course_offering_id": course_id,
                    "location_id": location_id,
                    "organizer_id": current_user.user_id,
                    "max_attendees": max_attendees,
                    "description": description,
                    "start_time": start_value,
                    "end_time": end_value,
                    "chill_level": chill_level,
                    "room_type_id": room_type_id,
                },
            )
            new_session_id = session_result.lastrowid
            if not new_session_id:
                new_session_id = db.session.execute(
                    queries.latest_session_id_query
                ).scalar()

            db.session.execute(
                queries.insert_attendance_query,
                {"user_id": current_user.user_id, "session_id": new_session_id},
            )

            if resource_name and resource_url:
                db.session.execute(
                    queries.insert_resource_query,
                    {
                        "session_id": new_session_id,
                        "uploaded_by": current_user.user_id,
                        "resource_name": resource_name,
                        "resource_url": resource_url,
                    },
                )

            if reminder_time:
                db.session.execute(
                    queries.insert_reminder_query,
                    {
                        "session_id": new_session_id,
                        "user_id": current_user.user_id,
                        "reminder_time": reminder_time.replace("T", " "),
                    },
                )

            for tag_id in tag_ids:
                db.session.execute(
                    queries.insert_session_tag_query,
                    {"session_id": new_session_id, "tag_id": tag_id},
                )

            db.session.commit()
            
            return redirect(url_for('view_session', session_id=new_session_id))
            
        return render_template("create_session.html", title="Create Session", room_types=fetch_all_room_types(), tags=fetch_all_tags())

    @app.route("/sessions/<int:session_id>")
    @login_required
    def view_session(session_id):

        checkOrganizer = False

        result = db.session.execute(
            queries.view_session_query, {"session_id": session_id}
        )
        row = result.fetchone()

        if not row:
            abort(404)
        
        if (current_user.user_id == row.organizer_id):
            checkOrganizer = True
        
        getOrganizerResult = db.session.execute(
            queries.fetch_user_by_id_query, {"user_id": row.organizer_id}
        )

        organizer = getOrganizerResult.fetchone()
        organizer_name = organizer.first_name + " " + organizer.last_name[0] + "."

        getAttendeesResult = db.session.execute(
            queries.fetch_all_attendees_query, {"session_id": session_id}
        )

        attendees = getAttendeesResult.fetchall()

        attendees_formatted = []
        for attendee in attendees:
            attendees_formatted.append(attendee.first_name + " " + attendee.last_init + ".")

        attendees_count = len(attendees_formatted)    
        
        print(attendees_formatted)

        # Build session dict with course and location
        session_dict = {
            'id': row.session_id,
            'session_id': row.session_id,
            'course_id': row.course_offering_id,
            'location_id': row.location_id,
            'organizer_id': row.organizer_id,
            'max_attendees': row.max_attendees,
            'description': row.description,
            'start_time': row.start_time.isoformat() if row.start_time else None,
            'end_time': row.end_time.isoformat() if row.end_time else None,
            'chill_level': row.chill_level,
            'room_type_id': row.room_type_id,
            'title': row.course_title or row.description or 'Study Session',
            'location': f"{row.location_address} - Room {row.location_room}" if row.location_address else 'TBD',
            'time': row.start_time.strftime('%b %d, %I:%M %p') if row.start_time else 'TBD',
            'attendees': str(attendees_count),
            'attendee_list': attendees_formatted,
            'organizer': organizer_name,
            'tag_ids': [],
            'resource_ids': [],
            'reminder_ids': []
        }
        
        # Build context for course and location details
        context = build_session_context(session_dict)

        return render_template(
            "session.html",
            session=context['session'],
            course=context['course'],
            location=context['location'],
            attendees=context['attendees'],
            isOrganizer=checkOrganizer,
        )

    @app.route("/sessions/<int:session_id>/resources", methods=['POST'])
    @login_required
    def upload_session_resource(session_id):
        session_record = find_session(session_id)
        if not session_record:
            abort(404)

        organizer_id = session_record.get('organizer_id')
        if organizer_id != current_user.user_id:
            flash('Only the session organizer can upload resources for now.', 'error')
            return redirect(url_for('view_session', session_id=session_id))

        resource_file = request.files.get('resource_file')
        if not resource_file or not resource_file.filename:
            flash('Please choose a text or PDF file to upload.', 'error')
            return redirect(url_for('view_session', session_id=session_id))

        filename = secure_filename(resource_file.filename)
        if '.' not in filename:
            flash('Resources must have a .txt or .pdf extension.', 'error')
            return redirect(url_for('view_session', session_id=session_id))

        extension = filename.rsplit('.', 1)[-1].lower()
        if extension not in ('txt', 'pdf'):
            flash('Resources must be a text or PDF file.', 'error')
            return redirect(url_for('view_session', session_id=session_id))

        fake_url = f"https://cdn.example.com/uploads/{filename}"

        db.session.execute(
            queries.insert_resource_query,
            {
                "session_id": session_id,
                "uploaded_by": current_user.user_id,
                "resource_name": filename,
                "resource_url": fake_url,
            },
        )
        db.session.commit()

        flash('Resource uploaded. The CDN link is a placeholder until storage is in place.', 'success')
        return redirect(url_for('view_session', session_id=session_id))

    @app.route("/join_session/<int:session_id>", methods=['POST'])
    @login_required
    def join_session(session_id):
        wants_json = request.headers.get("X-Requested-With") == "XMLHttpRequest"

        session_row = db.session.execute(
            queries.session_exists_query, {"session_id": session_id}
        ).first()
        if not session_row:
            message = "That session does not exist."
            if wants_json:
                return jsonify({"success": False, "message": message}), 404
            flash(message, "error")
            return redirect(url_for("home"))

        already_joined = db.session.execute(
            queries.attendance_exists_query,
            {"session_id": session_id, "user_id": current_user.user_id},
        ).first()
        if already_joined:
            message = "You already joined this session."
            if wants_json:
                return jsonify({"success": False, "message": message}), 400
            flash(message, "info")
            return redirect(url_for("home"))

        try:
            db.session.execute(
                queries.insert_attendance_query,
                {"session_id": session_id, "user_id": current_user.user_id},
            )
            db.session.commit()
        except Exception:
            db.session.rollback()
            current_app.logger.exception("Failed to join session %s", session_id)
            message = "Could not join that session. Please try again."
            if wants_json:
                return jsonify({"success": False, "message": message}), 500
            flash(message, "error")
            return redirect(url_for("home"))

        if wants_json:
            return jsonify({"success": True, "session_id": session_id})

        flash("Thanks for joining the session!", "success")
        return redirect(url_for("home"))
    
    @app.route("/leave_session/<int:session_id>", methods=['POST'])
    @login_required
    def leave_session(session_id):
        result = db.session.execute(
            queries.delete_attendance_query,
            {"session_id": session_id, "user_id": current_user.user_id},
        )
        db.session.commit()

        if result.rowcount:
            return jsonify(
                {"success": True, "message": "Successfully left the session"}
            )
        return jsonify({"success": False, "message": "Session not found"}), 404

    @app.route("/sessions/<int:session_id>/edit", methods=['GET', 'POST'])
    @login_required
    def edit_session(session_id):
        result = db.session.execute(
            queries.view_session_query, {"session_id": session_id}
        )
        row = result.fetchone()

        if not row:
            abort(404)

        if current_user.user_id != row.organizer_id:
            flash('Only the organizer can edit this session.', 'error')
            return redirect(url_for('view_session', session_id=session_id))

        if request.method == 'POST':
            course_id = request.form.get('course_id', type=int)
            location_id = request.form.get('location_id', type=int)
            max_attendees = request.form.get('max_attendees', type=int)
            description = request.form.get('description')
            start_time = request.form.get('start_time')
            end_time = request.form.get('end_time')
            chill_level = request.form.get('chill_level', type=int)
            room_type_id = request.form.get('room_type_id', type=int)
            tag_ids = []
            for raw_tag in request.form.getlist('tags'):
                tag_ids.append(int(raw_tag))

            if not course_id or not location_id:
                flash('Please pick a course and location from the list.', 'error')
                return redirect(request.url)

            if not max_attendees or not description or not start_time or not end_time or not chill_level or not room_type_id:
                flash('All required fields must be filled out.', 'error')
                return redirect(request.url)

            start_value = start_time.replace("T", " ")
            end_value = end_time.replace("T", " ")

            db.session.execute(
                queries.update_session_query,
                {
                    "session_id": session_id,
                    "course_id": course_id,
                    "location_id": location_id,
                    "max_attendees": max_attendees,
                    "description": description,
                    "start_time": start_value,
                    "end_time": end_value,
                    "chill_level": chill_level,
                    "room_type_id": room_type_id,
                },
            )

            db.session.execute(
                queries.delete_session_tags_query,
                {"session_id": session_id}
            )

            for tag_id in tag_ids:
                db.session.execute(
                    queries.insert_session_tag_query,
                    {"session_id": session_id, "tag_id": tag_id},
                )

            db.session.commit()
            
            flash('Session updated successfully!', 'success')
            return redirect(url_for('view_session', session_id=session_id))

        session_dict = {
            'id': row.session_id,
            'course_id': row.course_offering_id,
            'location_id': row.location_id,
            'organizer_id': row.organizer_id,
            'max_attendees': row.max_attendees,
            'description': row.description,
            'start_time': row.start_time.strftime('%Y-%m-%dT%H:%M') if row.start_time else '',
            'end_time': row.end_time.strftime('%Y-%m-%dT%H:%M') if row.end_time else '',
            'chill_level': row.chill_level,
            'room_type_id': row.room_type_id,
        }

        course = find_course(row.course_offering_id)
        location = find_location(row.location_id)
        session_tag_ids = get_session_tag_ids(session_id)
        
        course_display = f"{course['title']} - Section {course['section']} ({course['professor_name']})" if course else ''
        location_display = f"{location['address']} - Room {location['room_number']}" if location else ''

        return render_template(
            "edit_session.html",
            session=session_dict,
            course_display=course_display,
            location_display=location_display,
            room_types=fetch_all_room_types(),
            tags=fetch_all_tags(),
            session_tag_ids=session_tag_ids
        )

    @app.route("/sessions/<int:session_id>/delete", methods=['POST'])
    @login_required
    def delete_session(session_id):
        result = db.session.execute(
            queries.view_session_query, {"session_id": session_id}
        )
        row = result.fetchone()

        if not row:
            abort(404)

        if current_user.user_id != row.organizer_id:
            flash('Only the organizer can delete this session.', 'error')
            return redirect(url_for('view_session', session_id=session_id))

        db.session.execute(
            queries.delete_session_attendance_query,
            {"session_id": session_id}
        )

        db.session.execute(
            queries.delete_session_tags_query,
            {"session_id": session_id}
        )

        db.session.execute(
            queries.delete_session_query,
            {"session_id": session_id}
        )

        db.session.commit()

        flash('Session deleted successfully!', 'success')
        return redirect(url_for('home'))

    # API endpoints for locations
    @app.route("/api/locations", methods=["GET"])
    @login_required
    def get_locations():
        query_value = request.args.get("q", "").lower()
        if query_value:
            locations = db.session.execute(
                queries.search_locations_query,
                {"pattern": f"%{query_value}%"},
            ).fetchall()
        else:
            locations = db.session.execute(
                queries.list_locations_query
            ).fetchall()

        return jsonify([dict(row._mapping) for row in locations])

    @app.route("/api/locations", methods=["POST"])
    @login_required
    def create_location():
        data = request.get_json()

        # Validate required fields
        if not data.get("address") or not data.get("room_number"):
            return (
                jsonify(
                    {
                        "success": False,
                        "message": "Address and room number are required",
                    }
                ),
                400,
            )

        # Validate field lengths
        if len(data["address"]) > 100:
            return (
                jsonify(
                    {
                        "success": False,
                        "message": "Address must be 100 characters or less",
                    }
                ),
                400,
            )
        if len(data["room_number"]) > 20:
            return (
                jsonify(
                    {
                        "success": False,
                        "message": "Room number must be 20 characters or less",
                    }
                ),
                400,
            )

        duplicate = db.session.execute(
            queries.location_duplicate_query,
            {
                "address": data["address"].lower(),
                "room": data["room_number"].lower(),
            },
        ).first()
        if duplicate:
            return (
                jsonify(
                    {"success": False, "message": "This location already exists"}
                ),
                409,
            )

        result = db.session.execute(
            queries.insert_location_query,
            {
                "address": data["address"],
                "room_number": data["room_number"],
                "created_by_user": current_user.user_id,
            },
        )
        db.session.commit()
        new_id = result.lastrowid
        if not new_id:
            new_id = db.session.execute(
                queries.latest_location_id_query
            ).scalar()

        new_location = {
            "id": new_id,
            "address": data["address"],
            "room_number": data["room_number"],
        }

        return jsonify({"success": True, "location": new_location})

    # API endpoints for course offerings
    @app.route("/api/courses", methods=["GET"])
    @login_required
    def get_courses():
        query_value = request.args.get("q", "").lower()
        if query_value:
            courses = db.session.execute(
                queries.search_courses_query,
                {"pattern": f"%{query_value}%"},
            ).fetchall()
        else:
            courses = db.session.execute(
                queries.list_courses_query
            ).fetchall()

        return jsonify([dict(row._mapping) for row in courses])

    @app.route("/api/courses", methods=["POST"])
    @login_required
    def create_course():
        data = request.get_json()

        # Validate required fields
        required_fields = ["title", "section", "year", "term", "professor_name"]
        for field in required_fields:
            if field not in data or not data[field]:
                return (
                    jsonify(
                        {
                            "success": False,
                            "message": f'{field.replace("_", " ").title()} is required',
                        }
                    ),
                    400,
                )

        # Validate field lengths
        if len(data["title"]) > 100:
            return (
                jsonify(
                    {
                        "success": False,
                        "message": "Title must be 100 characters or less",
                    }
                ),
                400,
            )
        if len(data["section"]) > 20:
            return (
                jsonify(
                    {
                        "success": False,
                        "message": "Section must be 20 characters or less",
                    }
                ),
                400,
            )
        if len(data["professor_name"]) > 50:
            return (
                jsonify(
                    {
                        "success": False,
                        "message": "Professor name must be 50 characters or less",
                    }
                ),
                400,
            )

        # Validate year and term
        try:
            year = int(data["year"])
            term = int(data["term"])
            if year < 2020 or year > 2100:
                return (
                    jsonify(
                        {
                            "success": False,
                            "message": "Year must be between 2020 and 2100",
                        }
                    ),
                    400,
                )
            if term not in [1, 2, 3]:
                return (
                    jsonify(
                        {
                            "success": False,
                            "message": "Term must be 1 (Fall), 2 (Spring), or 3 (Summer)",
                        }
                    ),
                    400,
                )
        except ValueError:
            return jsonify({"success": False, "message": "Invalid year or term"}), 400

        duplicate = db.session.execute(
            queries.course_duplicate_query,
            {
                "title": data["title"].lower(),
                "section": data["section"].lower(),
                "year": year,
                "term": term,
            },
        ).first()
        if duplicate:
            return (
                jsonify(
                    {
                        "success": False,
                        "message": "This course offering already exists",
                    }
                ),
                409,
            )

        result = db.session.execute(
            queries.insert_course_offering_query,
            {
                "title": data["title"],
                "section": data["section"],
                "year": year,
                "term": term,
                "professor_name": data["professor_name"],
                "created_by_user": current_user.user_id,
            },
        )
        db.session.commit()
        new_id = result.lastrowid
        if not new_id:
            new_id = db.session.execute(
                queries.latest_course_id_query
            ).scalar()

        new_course = {
            "id": new_id,
            "title": data["title"],
            "section": data["section"],
            "year": year,
            "term": term,
            "professor_name": data["professor_name"],
        }

        return jsonify({"success": True, "course": new_course})

    @app.route("/404")
    def show_not_found():
        return render_template("errors/404.html"), 404

    @app.errorhandler(404)
    def handle_not_found(error):
        return render_template("errors/404.html"), 404

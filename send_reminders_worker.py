import os
import smtplib
from email.mime.text import MIMEText

from __init__ import create_app, db
import sql_queries as queries


def send_email(to_address, subject, body):
    gmail_user = os.getenv("GMAIL_USER") or os.getenv("GMAIL_USERNAME")
    gmail_pass = os.getenv("GMAIL_PASS") or os.getenv("GMAIL_PASSWORD")
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = gmail_user
    msg["To"] = to_address
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(gmail_user, gmail_pass)
        server.sendmail(gmail_user, [to_address], msg.as_string())
    return True


def main():
    app = create_app()
    with app.app_context():
        rows = db.session.execute(queries.due_reminders_query).fetchall()
        sent = 0
        for row in rows:
            start_time = row.start_time.strftime("%b %d, %I:%M %p")
            subject = "Study session reminder"
            body = f"Your study session is starting at {start_time}.\n\nDetails: {row.description}"
            if send_email(row.email, subject, body):
                db.session.execute(
                    queries.mark_reminder_sent_query,
                    {"reminder_id": row.reminder_id},
                )
                sent += 1
        db.session.commit()
        print(f"Sent Reminders For This Execution: {sent}")


if __name__ == "__main__":
    main()

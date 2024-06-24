from celery import shared_task
from datetime import datetime

from app.models import Task, User
from app import mongo_db
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os


class EmailHelper:
    def __init__(self):
        self.smtp_server = "smtp.freesmtpservers.com"
        self.smtp_port = 25
        self.smtp_username = os.environ.get("SMTP_USERNAME")
        self.smtp_password = os.environ.get("SMTP_PASSWORD")
        self.sender_email = "yaman.0.awad@gmail.com"

    def send_email(self, to_email, subject, body):
        message = MIMEMultipart()
        message["From"] = self.sender_email
        message["To"] = to_email
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain"))

        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_username, self.smtp_password)
                server.send_message(message)
            print(f"Email sent successfully to {to_email}")
            return True
        except Exception as e:
            print(f"Failed to send email: {str(e)}")
            return False

@shared_task
def send_task_notification(task_id, action):
    task = Task.query.get(task_id)
    user = User.query.get(task.user_id)

    # Prepare email content
    subject = f"Task Notification: {task.name} {action}"
    body = f"Your task '{task.name}' has been {action}."

    # Send email using EmailHelper
    email_helper = EmailHelper()
    email_sent = email_helper.send_email(user.email, subject, body)

    if email_sent:
        print(f"Email notification sent to {user.email} for task {task.name} {action}")
    else:
        print(f"Failed to send email notification to {user.email} for task {task.name} {action}")

    # Log the event in MongoDB
    mongo_db.logs.insert_one({
        'timestamp': datetime.utcnow(),
        'action': action,
        'task_id': task_id,
        'user_id': user.id,
        'email_sent': email_sent
    })
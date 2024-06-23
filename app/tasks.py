from app import celery, mongo_db
from app.models import Task, User
from datetime import datetime
from email_helper import EmailHelper


@celery.task
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
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
# src/email_alert.py

import smtplib
from email.message import EmailMessage

def send_alert_email(to_email, subject, body, smtp_server='smtp.gmail.com', port=587,
                     login='your_email@gmail.com', password='your_email_password'):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = login
    msg['To'] = to_email
    msg.set_content(body)

    try:
        with smtplib.SMTP(smtp_server, port) as smtp:
            smtp.starttls()
            smtp.login(login, password)
            smtp.send_message(msg)
        print("Alert email sent.")
    except Exception as e:
        print(f"Failed to send email: {e}")


# src/email_alert.py

def send_alert_email(to_email, subject, body, smtp_server='smtp.gmail.com', port=587,
                     login=None, password=None):
    if not login or not password:
        raise ValueError("Email login and password must be provided.")

    import smtplib
    from email.mime.text import MIMEText

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = login
    msg['To'] = to_email

    try:
        with smtplib.SMTP(smtp_server, port) as server:
            server.starttls()
            server.login(login, password)
            server.send_message(msg)
    except Exception as e:
        print(f"Failed to send alert email: {e}")



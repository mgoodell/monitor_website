# src/monitor.py

import requests, time
from queue import Queue
from src.email_alert import send_alert_email

log_queue = Queue()

def check_website_loop(url, interval, log_queue, email, email_password):
    while True:
        try:
            response = requests.get(url, timeout=5)
            status = f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {url} is UP"
        except requests.RequestException as e:
            status = f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {url} is DOWN ({e})"

            login = email
            password = email_password

            # Send email alert
            send_alert_email(
                to_email="michael.goodell@webinar.net",
                subject=f"ALERT: Website Down - {url}",
                body=f"The website {url} appears to be DOWN.\n\nError: {e}"
            )

        log_queue.put(status)
        time.sleep(interval)



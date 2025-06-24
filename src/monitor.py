# src/monitor.py

import requests
import time
from src.email_alert import send_alert_email  # Adjust import as needed

def check_website_loop(url, interval, log_queue, email, email_password):
    while True:
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(url, timeout=10, headers=headers)

            # Check if response is a 2xx status
            response.raise_for_status()

            status = f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {url} is UP"
        except requests.RequestException as e:
            status = f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {url} is DOWN ({e})"

            # Send email alert
            send_alert_email(
                to_email="michael.goodell@webinar.net",
                subject=f"ALERT: Website Down - {url}",
                body=f"The website {url} appears to be DOWN.\n\nError: {e}",
                login=email,
                password=email_password
            )

        log_queue.put(status)
        time.sleep(interval)



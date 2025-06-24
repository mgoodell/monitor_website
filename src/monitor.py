# src/monitor.py

import requests
import time
from src.email_alert import send_alert_email

# 1. It retries up to 3 times with increasing delay (2s, 4s, 8s) before declaring "DOWN".
# 2. Alerts are still sent once per outage.
# 3. Helps avoid false alarms due to brief hiccups.

def check_website_loop(url, interval, log_queue, email, email_password):
    was_down = False  # Track if it was down in previous check
    max_retries = 3
    base_delay = 2  # seconds

    while True:
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}

            # Retry logic with backoff
            for attempt in range(max_retries):
                try:
                    response = requests.get(url, timeout=10, headers=headers)
                    response.raise_for_status()  # Raise for 4xx/5xx
                    break  # success, exit retry loop
                except requests.RequestException as e:
                    if attempt == max_retries - 1:
                        raise  # Exhausted retries, raise last exception
                    else:
                        time.sleep(base_delay * (2 ** attempt))  # exponential backoff

            # If no exception, status is UP
            status = f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {url} is UP"
            was_down = False  # Reset flag

        except requests.RequestException as e:
            # Final failure after retries
            status = f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {url} is DOWN ({e})"
            if not was_down:
                send_alert_email(
                    to_email=email,
                    subject=f"ALERT: Website Down - {url}",
                    body=f"The website {url} appears to be DOWN after {max_retries} attempts.\n\nError: {e}",
                    login=email,
                    password=email_password
                )
                was_down = True

        log_queue.put(status)
        time.sleep(interval)



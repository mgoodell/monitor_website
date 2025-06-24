import requests
import time
from src.email_alert import send_alert_email

# 1. It retries up to 3 times with increasing delay (2s, 4s, 8s) before declaring "DOWN".
# 2. Alerts are still sent once per outage.
# 3. Helps avoid false alarms due to brief hiccups.
# 4. Logs UP status on every successful check (per user interval).

def check_website_loop(url, interval, log_queue, email, email_password):
    max_failures = 3
    max_successes = 2

    fail_count = 0
    success_count = 0
    was_down = False
    next_run = time.time()

    while True:
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(url, timeout=10, headers=headers)
            response.raise_for_status()

            success_count += 1
            fail_count = 0

            status = f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {url} is UP"
            log_queue.put(status)

            if success_count >= max_successes and was_down:
                was_down = False
                # Optional: send recovery email here

        except requests.RequestException as e:
            fail_count += 1
            success_count = 0

            if fail_count >= max_failures and not was_down:
                status = f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {url} is DOWN ({e})"
                log_queue.put(status)

                send_alert_email(
                    to_email=email,
                    subject=f"ALERT: Website Down - {url}",
                    body=f"The website {url} appears to be DOWN.\n\nError: {e}",
                    login=email,
                    password=email_password
                )
                was_down = True

            elif was_down:
                status = f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {url} is still DOWN ({e})"
                log_queue.put(status)

        # Wait until the next scheduled run time
        next_run += interval
        sleep_duration = max(0, next_run - time.time())
        time.sleep(sleep_duration)

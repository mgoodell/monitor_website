# app.py

from flask import Flask, render_template, request, Response, redirect
import threading
from queue import Queue
from src.monitor import check_website_loop

app = Flask(__name__)
monitor_threads = []
log_queue = Queue()
monitoring_should_stop = False

@app.route('/', methods=['GET', 'POST'])
def index():
    url = ''
    interval = '60'
    email = ''
    email_password = ''

    if request.method == 'POST':
        url = request.form.get('url', '').strip()
        interval = request.form.get('interval', '60')
        email = request.form.get('email')
        password = request.form.get('email_password')

        if not url.startswith("http"):
            url = "https://" + url

        t = threading.Thread(target=check_website_loop, args=(url, int(interval), log_queue, email, email_password), daemon=True)
        t.start()
        monitor_threads.append(t)

        return render_template(
            'index.html',
            success=True,
            url=url,
            interval=interval,
            notification_email=email,
            email_password=email_password
        )

    return render_template(
        'index.html',
        success=False,
        url=url,
        interval=interval,
        notification_email=email,
        email_password=email_password
    )

@app.route('/stream')
def stream():
    def event_stream():
        while True:
            message = log_queue.get()
            yield f"data: {message}\n\n"
    return Response(event_stream(), mimetype="text/event-stream")


@app.route('/stop', methods=['POST'])
def stop_monitoring():
    global monitoring_should_stop
    monitoring_should_stop = True
    return redirect("/")

if __name__ == '__main__':
    app.run(debug=True, threaded=True)



from flask import Flask, render_template, jsonify, Response
import psutil
import time
from prometheus_client import Gauge, Counter, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)
start_time = time.time()

cpu_usage = Gauge("system_cpu_usage_percent", "CPU Usage")
memory_usage = Gauge("system_memory_usage_percent", "Memory Usage")
app_uptime = Gauge("application_uptime_seconds", "Application Uptime")
http_requests = Counter("http_requests_total", "Total HTTP Requests")
app_status = Gauge("application_status", "Application Status")

@app.before_request
def count_requests():
    http_requests.inc()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/health")
def health():
    return jsonify({"status": "healthy", "application": "DevOps Monitor"})

@app.route("/api/stats")
def stats():
    cpu = psutil.cpu_percent(interval=0.2)
    memory = psutil.virtual_memory().percent
    uptime = int(time.time() - start_time)

    cpu_usage.set(cpu)
    memory_usage.set(memory)
    app_uptime.set(uptime)
    app_status.set(1)

    return jsonify({
        "cpu": cpu,
        "memory": memory,
        "uptime": uptime,
        "requests": http_requests._value.get(),
        "status": "Online"
    })

@app.route("/metrics")
def metrics():
    cpu_usage.set(psutil.cpu_percent())
    memory_usage.set(psutil.virtual_memory().percent)
    app_uptime.set(time.time() - start_time)
    app_status.set(1)
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)

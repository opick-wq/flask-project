from flask import Flask, jsonify, request
from prometheus_client import Counter, Histogram, generate_latest
import time

app = Flask(__name__)

# Metrik untuk observabilitas
REQUEST_COUNT = Counter(
    'app_request_count_total',
    'Total App Requests',
    ['method', 'endpoint', 'http_status']
)
REQUEST_LATENCY = Histogram(
    'app_request_latency_seconds',
    'Request latency',
    ['endpoint']
)

# Data dummy untuk API
items = [{"id": 1, "name": "laptop"}, {"id": 2, "name": "mouse"}]

# Middleware untuk mencatat metrik setiap request
@app.before_request
def start_timer():
    request.start_time = time.time()

@app.after_request
def record_metrics(response):
    latency = time.time() - request.start_time
    REQUEST_LATENCY.labels(request.path).observe(latency)
    REQUEST_COUNT.labels(request.method, request.path, response.status_code).inc()
    return response

# Endpoints Aplikasi
@app.route('/')
def home():
    REQUEST_COUNT.labels('GET', '/', 200).inc() # Increment manually for simple endpoint
    return "Welcome to the Simple Flask API!"

@app.route('/data', methods=['GET'])
def get_data():
    return jsonify(items)

@app.route('/data', methods=['POST'])
def add_data():
    new_item = request.get_json()
    items.append(new_item)
    return jsonify(new_item), 201

# Endpoint untuk Prometheus
@app.route('/metrics')
def metrics():
    return generate_latest().decode("utf-8")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
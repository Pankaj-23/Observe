from flask import Flask, jsonify
import psutil

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        "message": "System Monitoring API",
        "available_routes": ["/api/system"]
    })

@app.route('/api/system')
def system():
    return jsonify({
        "cpu": psutil.cpu_percent(),
        "memory": psutil.virtual_memory()._asdict(),
        "disk": psutil.disk_usage('/')._asdict()
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

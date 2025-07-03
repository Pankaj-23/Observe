import os
from flask import Flask, render_template
from dotenv import load_dotenv
from utils import get_incident_counts

# Load .env variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

@app.route('/')
def dashboard():
    try:
        counts = get_incident_counts()
        return render_template("dashboard.html", counts=counts)
    except Exception as e:
        return f"Error: {str(e)}", 500

if __name__ == "__main__":
    app.run(debug=True)

import subprocess
import threading
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def run_flask_app():
    """Run Flask app."""
    app.run(debug=False, host='0.0.0.0', port=5000)  # Disable debug mode to avoid reloader issues

if __name__ == "__main__":
    # Start Flask app in a separate thread.
    flask_thread = threading.Thread(target=run_flask_app)
    flask_thread.start()

    print("Flask app running at http://127.0.0.1:5000/")

    # Start LiveKit agents (main.py) in a separate process.
    subprocess.Popen(['python3', 'main.py', 'start'])

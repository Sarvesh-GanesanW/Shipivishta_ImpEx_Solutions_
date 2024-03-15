from flask import Flask, render_template
import logging
import os
from dotenv import load_dotenv
from routes import init_routes
from admin import setup_admin  # Import setup_admin from admin.py

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Set the secret key for CSRF protection
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

logging.basicConfig(level=logging.DEBUG)

@app.route('/')
def hello_world():
    try:
        logging.info("Accessed the root route")
        return render_template('index.html')
    except Exception as e:
        logging.error("Error accessing the root route: %s", e, exc_info=True)
        return "An error occurred", 500

@app.after_request
def set_csp_header(response):
    response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self' https://code.jquery.com https://cdnjs.cloudflare.com https://stackpath.bootstrapcdn.com; style-src 'self' https://stackpath.bootstrapcdn.com;"
    return response

# Initialize routes from the routes module
try:
    init_routes(app)
    logging.info("Routes initialized successfully.")
except Exception as e:
    logging.error("Failed to initialize routes: %s", e, exc_info=True)

# Setup Flask-Admin
try:
    setup_admin(app)
    logging.info("Flask-Admin setup successfully.")
except Exception as e:
    logging.error("Failed to setup Flask-Admin: %s", e, exc_info=True)

if __name__ == '__main__':
    try:
        app.run(port=8000, ssl_context=('cert.pem', 'key.pem'))
        logging.info("Starting the application on port 8000 with HTTPS")
    except Exception as e:
        logging.error("Failed to start the application: %s", e, exc_info=True)
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Log all environment variables
print(f"All environment variables: {os.environ}")

# Set up the database connection
DATABASE_URL = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Import and register routes
from routes import api
app.register_blueprint(api)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)

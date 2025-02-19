from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Set up the database connection
DATABASE_URL = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Define the Notification model
class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50), nullable=False)
    message = db.Column(db.String(255), nullable=False)

# Route to get notifications by type
@app.route('/get_notifications/<notification_type>', methods=['GET'])
def get_notifications_by_type(notification_type):
    """Retrieves all notifications of a specific type."""
    notifications = Notification.query.filter_by(type=notification_type).all()
    if not notifications:
        return jsonify({"error": "No notifications found for this type"}), 404

    return jsonify({"notifications": [n.message for n in notifications]})

# Route to get all notifications
@app.route('/get_all_notifications', methods=['GET'])
def get_all_notifications():
    """Retrieves all notifications in the database."""
    notifications = Notification.query.all()
    return jsonify({"notifications": [{"type": n.type, "message": n.message} for n in notifications]})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)

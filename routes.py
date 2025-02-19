from flask import Blueprint, jsonify
from models import Notification
from app import db

# Define a Blueprint for routes
api = Blueprint('api', __name__)


@api.route('/get_notifications/<notification_type>', methods=['GET'])
def get_notifications_by_type(notification_type):
    """Retrieves all notifications of a specific type."""
    notifications = Notification.query.filter_by(type=notification_type).all()
    if not notifications:
        return jsonify({"error": "No notifications found for this type"}), 404

    return jsonify({"notifications": [n.message for n in notifications]})


@api.route('/get_all_notifications', methods=['GET'])
def get_all_notifications():
    """Retrieves all notifications in the database."""
    notifications = Notification.query.all()
    return jsonify({"notifications": [{"type": n.type, "message": n.message} for n in notifications]})

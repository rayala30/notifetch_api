from flask import Blueprint, jsonify, request
from models import Notification
from app import db

# Define a Blueprint for routes
api = Blueprint('api', __name__)


@api.route("/")
def home():
    return jsonify({"message": "Welcome to NotiFetch API!"})


@api.route('/notifications/<notification_type>', methods=['GET'])
def get_notifications_by_type(notification_type):
    """Retrieves all notifications of a specific type, allowing dynamic placeholders."""
    notifications = Notification.query.filter_by(type=notification_type).all()

    if not notifications:
        return jsonify({"error": "No notifications found for this type"}), 404

    # Get custom values passed in request
    custom_values = request.args.to_dict()

    # Replace placeholders with actual values provided in the request
    processed_notifications = []
    for n in notifications:
        try:
            message = n.template.format(**custom_values)
        except KeyError as e:
            message = f"Missing data: {str(e)[1:-1]}"
        processed_notifications.append(message)

    return jsonify({"notifications": processed_notifications})


@api.route('/notifications', methods=['GET'])
def get_all_notifications():
    """Retrieves all notifications in the database."""
    notifications = Notification.query.all()
    return jsonify({"notifications": [{"type": n.type, "template": n.template} for n in notifications]})

from flask import Blueprint, jsonify, request
from models import Notification
from app import db
import re
import logging

# Define a Blueprint for routes
api = Blueprint('api', __name__)


@api.route("/")
def home():
    return jsonify({"message": "Welcome to NotiFetch API!"})


@api.route('/notifications/<notification_type>', methods=['GET'])
def get_notifications_by_type(notification_type):
    """Retrieves all notifications of a specific type."""
    notifications = Notification.query.filter_by(type=notification_type).all()

    if not notifications:
        return jsonify({"error": "No notifications found for this type"}), 404

    return jsonify({"notifications": [{"id": n.id, "type": n.type, "template": n.template} for n in notifications]})


@api.route('/notifications/<int:notification_id>', methods=['GET'])
def get_notification_by_id(notification_id):
    """Retrieves a single notification by its ID."""
    notification = Notification.query.get(notification_id)

    if not notification:
        return jsonify({"error": "Notification not found"}), 404

    return jsonify({"id": notification.id, "type": notification.type, "template": notification.template})


@api.route('/notifications', methods=['GET'])
def get_all_notifications():
    """Retrieves all notifications in the database."""
    notifications = Notification.query.all()
    return jsonify({"notifications": [{"id": n.id, "type": n.type, "template": n.template} for n in notifications]})


@api.route('/notifications/<int:notification_id>/fields', methods=['GET'])
def get_notification_placeholders(notification_id):
    """Retrieves all required fields (placeholders) for a notification template."""
    notification = Notification.query.get(notification_id)

    if not notification:
        return jsonify({"error": "Notification not found"}), 404

    # Extract placeholders from the template (e.g., "{item_name}")
    placeholders = re.findall(r'\{(.*?)\}', notification.template)

    return jsonify({"id": notification.id, "template": notification.template, "type": notification.type, "placeholders": placeholders})



from app import db


class Notification(db.Model):
    __tablename__ = 'notifications'  # Ensure this matches your table name in the DB

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50), nullable=False)
    template = db.Column(db.String(255), nullable=False)

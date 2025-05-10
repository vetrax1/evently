from flask import Blueprint, jsonify, request
from .models import Event, Booking
from .db import db
from .utils import can_book
from datetime import datetime

api_blueprint = Blueprint('api', __name__)

@api_blueprint.route("/api/events", methods=["GET"])
def list_events():
    events = Event.query.all()
    return jsonify([
        {
            "id": e.id,
            "title": e.title,
            "location": e.location,
            "date": e.date.strftime("%Y-%m-%d %H:%M"),
            "total_seats": e.total_seats,
            "booked_seats": e.booked_seats,
            "remaining_seats": e.remaining_seats()
        } for e in events
    ]), 200

@api_blueprint.route("/api/events", methods=["POST"])
def create_event():
    data = request.get_json()
    try:
        event = Event(
            title=data["title"],
            location=data["location"],
            date=datetime.strptime(data["date"], "%Y-%m-%dT%H:%M"),
            total_seats=int(data["total_seats"])
        )
        db.session.add(event)
        db.session.commit()
        return jsonify({"message": "Event created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@api_blueprint.route("/api/book/<int:event_id>", methods=["POST"])
def book_event(event_id):
    event = Event.query.get_or_404(event_id)
    if not can_book(event):
        return jsonify({"error": "No seats available"}), 400

    data = request.get_json()
    booking = Booking(
        event_id=event_id,
        name=data["name"],
        email=data["email"]
    )
    event.booked_seats += 1
    db.session.add(booking)
    db.session.commit()
    return jsonify({"message": "Booking successful"}), 201

@api_blueprint.route("/api/cancel/<int:event_id>", methods=["POST"])
def cancel_booking(event_id):
    data = request.get_json()
    booking = Booking.query.filter_by(event_id=event_id, email=data["email"]).first()
    if not booking:
        return jsonify({"error": "Booking not found"}), 404

    event = Event.query.get(event_id)
    event.booked_seats -= 1
    db.session.delete(booking)
    db.session.commit()
    return jsonify({"message": "Booking canceled"}), 200

@api_blueprint.route("/api/events/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
    event = Event.query.get(event_id)
    if not event:
        return jsonify({"error": "Event not found"}), 404

    # Also delete associated bookings
    Booking.query.filter_by(event_id=event.id).delete()
    db.session.delete(event)
    db.session.commit()
    return jsonify({"message": "Event deleted"}), 200


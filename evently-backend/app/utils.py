def can_book(event):
    return event.booked_seats < event.total_seats

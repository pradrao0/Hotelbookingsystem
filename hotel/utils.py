from django.core.mail import send_mail


def send_booking_email(email, booking):
    subject = "Booking Confirmed"

    message = f"""
    Your booking is confirmed!

    Room: {booking.room.room_number}
    Check-in: {booking.check_in_date}
    Check-out: {booking.check_out_date}
    Total Price: {booking.total_price}
    """

    send_mail(
        subject,
        message,
        "noreply@hotel.com",
        [email],
        fail_silently=True
    )
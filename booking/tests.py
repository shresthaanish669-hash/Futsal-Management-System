from datetime import time
from decimal import Decimal
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase
from .models import Booking, Court, Venue


class BookingConflictTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("player", password="safe-password-123")
        venue = Venue.objects.create(name="Test Ground", address="Kathmandu", phone="9800000000")
        self.court = Court.objects.create(venue=venue, name="Court A", price_per_hour=Decimal("2000"))

    def test_overlapping_active_booking_is_rejected(self):
        Booking.objects.create(court=self.court, customer=self.user, booking_date="2030-01-10", start_time=time(18), end_time=time(19), total_price=2000)
        overlap = Booking(court=self.court, customer=self.user, booking_date="2030-01-10", start_time=time(18, 30), end_time=time(19, 30), total_price=2000)
        with self.assertRaises(ValidationError):
            overlap.full_clean()


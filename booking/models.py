from decimal import Decimal
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class Venue(models.Model):
    name = models.CharField(max_length=120)
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=25)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="venues")
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Court(models.Model):
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, related_name="courts")
    name = models.CharField(max_length=80)
    surface = models.CharField(max_length=80, default="Artificial turf")
    capacity = models.PositiveIntegerField(default=10)
    price_per_hour = models.DecimalField(max_digits=9, decimal_places=2, default=Decimal("2000.00"))
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["venue", "name"]
        constraints = [models.UniqueConstraint(fields=["venue", "name"], name="unique_court_name_per_venue")]

    def __str__(self):
        return f"{self.venue.name} — {self.name}"


class Team(models.Model):
    name = models.CharField(max_length=100)
    captain = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="captained_teams")
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="teams", blank=True)
    home_area = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Booking(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending payment"
        CONFIRMED = "confirmed", "Confirmed"
        CANCELLED = "cancelled", "Cancelled"

    court = models.ForeignKey(Court, on_delete=models.PROTECT, related_name="bookings")
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="bookings")
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True, related_name="bookings")
    booking_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    total_price = models.DecimalField(max_digits=9, decimal_places=2)
    status = models.CharField(max_length=12, choices=Status.choices, default=Status.PENDING)
    notes = models.CharField(max_length=240, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["booking_date", "start_time"]

    def clean(self):
        if self.start_time and self.end_time and self.start_time >= self.end_time:
            raise ValidationError("End time must be after the start time.")
        if self.court_id and self.booking_date and self.start_time and self.end_time:
            conflicts = Booking.objects.filter(
                court=self.court,
                booking_date=self.booking_date,
                status__in=[self.Status.PENDING, self.Status.CONFIRMED],
            ).exclude(pk=self.pk).filter(start_time__lt=self.end_time, end_time__gt=self.start_time)
            if conflicts.exists():
                raise ValidationError("That time overlaps with an existing booking. Please choose another slot.")

    @property
    def reference(self):
        return f"FM-{self.pk:05d}" if self.pk else "FM-DRAFT"

    def __str__(self):
        return f"{self.reference} · {self.court}"


class Payment(models.Model):
    class Method(models.TextChoices):
        CASH = "cash", "Cash"
        ESEWA = "esewa", "eSewa"
        KHALTI = "khalti", "Khalti"
        CARD = "card", "Card"

    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name="payment")
    amount = models.DecimalField(max_digits=9, decimal_places=2)
    method = models.CharField(max_length=12, choices=Method.choices, default=Method.CASH)
    paid_at = models.DateTimeField(default=timezone.now)
    transaction_id = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"Payment for {self.booking.reference}"


class Tournament(models.Model):
    name = models.CharField(max_length=150)
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, related_name="tournaments")
    start_date = models.DateField()
    end_date = models.DateField()
    registration_fee = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    max_teams = models.PositiveIntegerField(default=8)
    teams = models.ManyToManyField(Team, blank=True, related_name="tournaments")
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["start_date"]

    def __str__(self):
        return self.name


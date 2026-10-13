# Generated manually for the starter project.
from decimal import Decimal
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):
    initial = True
    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
        migrations.CreateModel(
            name="Venue",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=120)),
                ("address", models.CharField(max_length=200)),
                ("phone", models.CharField(max_length=25)),
                ("description", models.TextField(blank=True)),
                ("is_active", models.BooleanField(default=True)),
                ("owner", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="venues", to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ["name"]},
        ),
        migrations.CreateModel(
            name="Team",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100)),
                ("home_area", models.CharField(blank=True, max_length=100)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("captain", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="captained_teams", to=settings.AUTH_USER_MODEL)),
                ("members", models.ManyToManyField(blank=True, related_name="teams", to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ["name"]},
        ),
        migrations.CreateModel(
            name="Court",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=80)),
                ("surface", models.CharField(default="Artificial turf", max_length=80)),
                ("capacity", models.PositiveIntegerField(default=10)),
                ("price_per_hour", models.DecimalField(decimal_places=2, default=Decimal("2000.00"), max_digits=9)),
                ("is_active", models.BooleanField(default=True)),
                ("venue", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="courts", to="booking.venue")),
            ],
            options={"ordering": ["venue", "name"]},
        ),
        migrations.CreateModel(
            name="Tournament",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=150)),
                ("start_date", models.DateField()),
                ("end_date", models.DateField()),
                ("registration_fee", models.DecimalField(decimal_places=2, default=0, max_digits=9)),
                ("max_teams", models.PositiveIntegerField(default=8)),
                ("description", models.TextField(blank=True)),
                ("teams", models.ManyToManyField(blank=True, related_name="tournaments", to="booking.team")),
                ("venue", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="tournaments", to="booking.venue")),
            ],
            options={"ordering": ["start_date"]},
        ),
        migrations.CreateModel(
            name="Booking",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("booking_date", models.DateField()),
                ("start_time", models.TimeField()),
                ("end_time", models.TimeField()),
                ("total_price", models.DecimalField(decimal_places=2, max_digits=9)),
                ("status", models.CharField(choices=[("pending", "Pending payment"), ("confirmed", "Confirmed"), ("cancelled", "Cancelled")], default="pending", max_length=12)),
                ("notes", models.CharField(blank=True, max_length=240)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("court", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="bookings", to="booking.court")),
                ("customer", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="bookings", to=settings.AUTH_USER_MODEL)),
                ("team", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="bookings", to="booking.team")),
            ],
            options={"ordering": ["booking_date", "start_time"]},
        ),
        migrations.CreateModel(
            name="Payment",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("amount", models.DecimalField(decimal_places=2, max_digits=9)),
                ("method", models.CharField(choices=[("cash", "Cash"), ("esewa", "eSewa"), ("khalti", "Khalti"), ("card", "Card")], default="cash", max_length=12)),
                ("paid_at", models.DateTimeField(default=django.utils.timezone.now)),
                ("transaction_id", models.CharField(blank=True, max_length=100)),
                ("booking", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="payment", to="booking.booking")),
            ],
        ),
        migrations.AddConstraint(
            model_name="court",
            constraint=models.UniqueConstraint(fields=("venue", "name"), name="unique_court_name_per_venue"),
        ),
    ]


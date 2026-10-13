from django.contrib import admin
from .models import Booking, Court, Payment, Team, Tournament, Venue


@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ("name", "address", "phone", "is_active")
    search_fields = ("name", "address")


@admin.register(Court)
class CourtAdmin(admin.ModelAdmin):
    list_display = ("name", "venue", "surface", "price_per_hour", "is_active")
    list_filter = ("venue", "is_active")


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("reference", "court", "customer", "booking_date", "start_time", "status", "total_price")
    list_filter = ("status", "booking_date", "court__venue")
    search_fields = ("customer__username", "court__name")


admin.site.register(Team)
admin.site.register(Payment)
admin.site.register(Tournament)


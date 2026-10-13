from datetime import datetime
from decimal import Decimal
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from .forms import BookingForm, SignUpForm, TeamForm
from .models import Booking, Court, Tournament, Venue


def home(request):
    venues = Venue.objects.filter(is_active=True).annotate(court_count=Count("courts"))[:3]
    return render(request, "booking/home.html", {"venues": venues})


def venue_list(request):
    venues = Venue.objects.filter(is_active=True).prefetch_related("courts")
    return render(request, "booking/venue_list.html", {"venues": venues})


def venue_detail(request, venue_id):
    venue = get_object_or_404(Venue, pk=venue_id, is_active=True)
    return render(request, "booking/venue_detail.html", {"venue": venue, "courts": venue.courts.filter(is_active=True)})


@login_required
def book_court(request, court_id):
    court = get_object_or_404(Court, pk=court_id, is_active=True, venue__is_active=True)
    if request.method == "POST":
        form = BookingForm(request.POST, user=request.user)
        form.instance.court = court
        form.instance.customer = request.user
        if form.is_valid():
            booking = form.save(commit=False)
            start = datetime.combine(booking.booking_date, booking.start_time)
            end = datetime.combine(booking.booking_date, booking.end_time)
            hours = Decimal(str((end - start).total_seconds() / 3600))
            booking.total_price = (hours * court.price_per_hour).quantize(Decimal("0.01"))
            booking.save()
            messages.success(request, f"Your slot request {booking.reference} is saved. Confirm payment at the venue to lock it in.")
            return redirect("booking_confirmation", booking_id=booking.id)
    else:
        form = BookingForm(user=request.user)
    reserved_slots = Booking.objects.filter(court=court, booking_date__gte=timezone.localdate(), status__in=[Booking.Status.PENDING, Booking.Status.CONFIRMED])[:8]
    return render(request, "booking/book_court.html", {"court": court, "form": form, "reserved_slots": reserved_slots})


@login_required
def booking_confirmation(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id, customer=request.user)
    return render(request, "booking/confirmation.html", {"booking": booking})


@login_required
def dashboard(request):
    bookings = Booking.objects.filter(customer=request.user).select_related("court__venue", "team")
    upcoming = bookings.filter(booking_date__gte=timezone.localdate()).order_by("booking_date", "start_time")
    teams = request.user.captained_teams.prefetch_related("members")
    return render(request, "booking/dashboard.html", {"bookings": upcoming, "teams": teams})


@login_required
def create_team(request):
    if request.method == "POST":
        form = TeamForm(request.POST)
        if form.is_valid():
            team = form.save(commit=False)
            team.captain = request.user
            team.save()
            team.members.add(request.user)
            messages.success(request, f"{team.name} is ready. Add players through the team section in admin for now.")
            return redirect("dashboard")
    else:
        form = TeamForm()
    return render(request, "booking/form_page.html", {"form": form, "title": "Create your team", "subtitle": "Build your squad for upcoming matches and tournaments.", "button_label": "Create team"})


def tournament_list(request):
    tournaments = Tournament.objects.select_related("venue").prefetch_related("teams")
    return render(request, "booking/tournaments.html", {"tournaments": tournaments})


def booking_calendar(request):
    date_string = request.GET.get("date")
    try:
        chosen_date = datetime.strptime(date_string, "%Y-%m-%d").date() if date_string else timezone.localdate()
    except ValueError:
        chosen_date = timezone.localdate()
    bookings = Booking.objects.filter(booking_date=chosen_date, status__in=[Booking.Status.PENDING, Booking.Status.CONFIRMED]).select_related("court__venue").order_by("start_time")
    return render(request, "booking/calendar.html", {"bookings": bookings, "chosen_date": chosen_date})


def signup(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Welcome to Kickoff. Your account is ready!")
            return redirect("dashboard")
    else:
        form = SignUpForm()
    return render(request, "registration/signup.html", {"form": form})


@login_required
def owner_report(request):
    venues = request.user.venues.all()
    if not venues.exists() and not request.user.is_staff:
        raise Http404
    bookings = Booking.objects.filter(court__venue__in=venues) if not request.user.is_staff else Booking.objects.all()
    stats = bookings.aggregate(total_sales=Sum("total_price"), total_bookings=Count("id"))
    by_venue = bookings.values("court__venue__name").annotate(bookings=Count("id"), sales=Sum("total_price")).order_by("-sales")
    return render(request, "booking/report.html", {"stats": stats, "by_venue": by_venue})


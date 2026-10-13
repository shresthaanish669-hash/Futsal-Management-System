from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("venues/", views.venue_list, name="venue_list"),
    path("venues/<int:venue_id>/", views.venue_detail, name="venue_detail"),
    path("courts/<int:court_id>/book/", views.book_court, name="book_court"),
    path("bookings/<int:booking_id>/confirmation/", views.booking_confirmation, name="booking_confirmation"),
    path("calendar/", views.booking_calendar, name="booking_calendar"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("teams/new/", views.create_team, name="create_team"),
    path("tournaments/", views.tournament_list, name="tournament_list"),
    path("reports/", views.owner_report, name="owner_report"),
    path("accounts/login/", auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
    path("accounts/signup/", views.signup, name="signup"),
    path("accounts/logout/", auth_views.LogoutView.as_view(), name="logout"),
]


from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Booking, Team


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("first_name", "username", "email", "password1", "password2")


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ("booking_date", "start_time", "end_time", "team", "notes")
        widgets = {
            "booking_date": forms.DateInput(attrs={"type": "date", "min": timezone.localdate().isoformat()}),
            "start_time": forms.TimeInput(attrs={"type": "time"}),
            "end_time": forms.TimeInput(attrs={"type": "time"}),
            "notes": forms.TextInput(attrs={"placeholder": "Optional: match name or special request"}),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields["team"].queryset = Team.objects.filter(captain=user)
        self.fields["team"].required = False

    def clean_booking_date(self):
        booking_date = self.cleaned_data["booking_date"]
        if booking_date < timezone.localdate():
            raise forms.ValidationError("Please select today or a future date.")
        return booking_date


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ("name", "home_area")
        widgets = {"name": forms.TextInput(attrs={"placeholder": "e.g. Thunder FC"})}


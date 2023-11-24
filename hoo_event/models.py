from django.db import models
from django import forms
from django.utils import timezone
from enum import Enum

# Create your models here.
from django.contrib.auth.models import Group, Permission
from django.core.exceptions import ValidationError

regular_users, created = Group.objects.get_or_create(name ='regular_users')
admin_users, created = Group.objects.get_or_create(name ='admin_users')

class EventStatus(Enum):
    PENDING = 1
    APPROVED = 2
    DENIED = 3

# Create your models here.
class EventForm(forms.Form):
    event_title = forms.CharField(max_length=100)
    event_description = forms.CharField(widget=forms.Textarea)
    event_capacity = forms.IntegerField()
    event_start_time = forms.DateTimeField()
    event_end_time = forms.DateTimeField()
    event_street_address = forms.CharField(max_length=100)
    event_city = forms.CharField(max_length=100)
    event_state = forms.CharField(max_length=100)


    # This source helped validate user input
    # https://stackoverflow.com/questions/8557885/validationerror-while-using-modelform-django
    def clean_event_state(self):
        state = self.cleaned_data['event_state']
        start = self.cleaned_data['event_start_time']
        end = self.cleaned_data['event_end_time']
        if start >= end:
            raise ValidationError("Please enter a start time that is before the end time")
        return state


class Event(models.Model):
    event_title = models.CharField(max_length=100)
    event_description = models.TextField()
    event_longitude = models.DecimalField(max_digits=9, decimal_places=6)
    event_latitude = models.DecimalField(max_digits=9, decimal_places=6)
    event_street_address = models.CharField(max_length=100)
    event_city = models.CharField(max_length=100)
    event_state = models.CharField(max_length=100)
    event_start_time = models.DateTimeField(default="2000-01-01T00:00")
    event_end_time = models.DateTimeField(default="2000-01-01T00:00")
    event_status = models.CharField(default=EventStatus.PENDING)
    event_email = models.CharField(max_length=100) # This is the email of the host
    event_capacity = models.PositiveIntegerField(default=0) # This one keeps track of the actual people who signed up
    event_full_capacity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.event_title


class HeadCount(models.Model):
    user_email = models.CharField(max_length=100)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user_email} is signed up for {self.event.event_title}"
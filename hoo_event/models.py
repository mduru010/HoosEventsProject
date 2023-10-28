from django.db import models
from django import forms
from django.utils import timezone

# Create your models here.
from django.contrib.auth.models import Group, Permission

regular_users, created = Group.objects.get_or_create(name ='regular_users')
admin_users, created = Group.objects.get_or_create(name ='admin_users')



# Create your models here.
class EventForm(forms.Form):
    event_title = forms.CharField(max_length=100)
    event_street_address = forms.CharField(max_length=100)
    event_city = forms.CharField(max_length=100)
    event_state = forms.CharField(max_length=100)
    event_start_time = forms.DateTimeField()
    event_end_time = forms.DateTimeField()
    # event_description = forms.CharField(widget=forms.Textarea)

class Event(models.Model):
    event_title = models.CharField(max_length=100)
    event_longitude = models.DecimalField(max_digits=9, decimal_places=6)
    event_latitude = models.DecimalField(max_digits=9, decimal_places=6)
    event_street_address = models.CharField(max_length=100)
    event_city = models.CharField(max_length=100)
    event_state = models.CharField(max_length=100)
    event_start_time = models.DateTimeField(default="2000-01-01T00:00")
    event_end_time = models.DateTimeField(default="2000-01-01T00:00")

    def __str__(self):
        return self.event_title

    # event_description = models.TextField()

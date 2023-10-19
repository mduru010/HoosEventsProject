# /***************************************************************************************
# *  REFERENCES
# *  Title: Using the Django authentication system
# *  Author: Django Documentation
# *  Date: October 7th, 2023
# *  Version: 4.2
# *  URL: https://docs.djangoproject.com/en/4.2/topics/auth/default/
# *
# *  Title: User group get method filter.exists
# *  Author: Charlesthk
# *  Date: October 18th, 2023
# *  URL: https://stackoverflow.com/questions/4789021/in-django-how-do-i-check-if-a-user-is-in-a-certain-group
# *
# ***************************************************************************************/


from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
import json
from django.conf import settings
from .models import EventForm, Event
import requests
from django.http import HttpResponseRedirect
import googlemaps

@login_required
def main(request):
    if request.user.groups.filter(name='admin_users').exists() or (request.user.email == "pointlssus1@gmail.com") or (request.user.email == "cs3240.super@gmail.com"):
        return redirect('admin_event')
    elif request.user.is_staff:
        return redirect('admin:index')
    elif request.user.groups.filter(name='regular_users').exists() or (request.user.email == "cs3240.student@gmail.com"):
        return redirect('index')
    return redirect('index') # delete once we properly define all users that sign up as regular users

def addEvent(request):
    form = EventForm()
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            
            event_title = form.cleaned_data['event_title']
            event_street_address = form.cleaned_data['event_street_address']
            event_city = form.cleaned_data['event_city']
            event_state = form.cleaned_data['event_state']
            event_time_start = form.cleaned_data['event_time_start']
            event_time_end = form.cleaned_data['event_time_end']
            event_description = form.cleaned_data['event_description']
            
            new_event = Event.objects.create(
                event_title = event_title,
                event_street_address = event_street_address,
                event_city = event_city,
                event_state = event_state,
                event_time_start = event_time_start,
                event_time_end = event_time_end,
                event_description = event_description
            )

            # Example call: https://maps.googleapis.com/maps/api/geocode/json?address=1600+Amphitheatre+Parkway,+Mountain+View,+CA&key=YOUR_API_KEY

            url = 'https://maps.googleapis.com/maps/api/geocode/json?'

            street_address_split = event_street_address.split(' ')
            street_address = ''
            for word in street_address_split:
                street_address += word + '+'

            city_split = event_city.split(' ')
            city = ''
            for word in city_split:
                city += word + '+'

            state_split = event_state.split(' ')
            state = ''
            for word in state_split:
                state += word + '+'

            address = street_address + "," + city + "," + state
            url += 'address=' + address + '&key=' + settings.GOOGLE_API_KEY

            response = requests.get(url)
            data = response.json()
            lat = data['results'][0]['geometry']['location']['lat']
            lng = data['results'][0]['geometry']['location']['lng']

            new_event.event_latitude = lat
            new_event.event_longitude = lng

            new_event.save()
            return HttpResponseRedirect(reversed('index'))

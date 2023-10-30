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


from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
import json
from django.conf import settings
from .models import EventForm, Event, EventStatus
import requests
from django.http import HttpResponseRedirect
from django.contrib.auth.models import Group, Permission
from django.urls import reverse
from django.utils import timezone
from django.views import generic
# import googlemaps

@login_required
def main(request):
    regular_users = Group.objects.get(name='regular_users')
    admin_users = Group.objects.get(name='admin_users')
    if request.user.email == "cs3240.student@gmail.com":
        regular_users.user_set.add(request.user)
    elif request.user.email == "cs3240.super@gmail.com":
        admin_users.user_set.add(request.user)
    if not request.user.groups.filter(name='admin_users').exists():
        regular_users.user_set.add(request.user)

    if request.user.is_staff:
        return redirect('admin:index')
    elif request.user.groups.filter(name='admin_users').exists():
        return redirect('admin_event')
    elif request.user.groups.filter(name='regular_users').exists():
        return redirect(reverse('hoo_event:index'))

def addEvent(request):
    form = EventForm()
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            event_title = form.cleaned_data['event_title']
            event_street_address = form.cleaned_data['event_street_address']
            event_city = form.cleaned_data['event_city']
            event_state = form.cleaned_data['event_state']
            event_start_time = form.cleaned_data['event_start_time']
            event_end_time = form.cleaned_data['event_end_time']
            # event_description = form.cleaned_data['event_description']
            print("start:", event_start_time)
            print("end:", event_end_time)

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

            new_event = Event.objects.create(
                event_title=event_title,
                event_latitude = lat,
                event_longitude = lng,
                event_street_address=event_street_address,
                event_city=event_city,
                event_state=event_state,
                event_start_time = event_start_time,
                event_end_time = event_end_time,
                event_status = EventStatus.PENDING,
                # event_description = event_description
            )
            print(lat, lng)

            new_event.save()
            return HttpResponseRedirect(reverse('hoo_event:index'))
        else:
            print(form.errors)

    return render(request, "hoo_event/create_event.html", {"form": form})

def event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    return render(request, 'event.html', {'event': event})

class ShowRecentView(generic.ListView):
    template_name = "hoo_event/recent_event.html"
    context_object_name = "latest_events"

    def get_queryset(self):
        """
        Get the most 5 recently added events
        """
        all_events = Event.objects.filter(event_status__exact=EventStatus.APPROVED)
        n = len(all_events)

        if n < 5:
            return all_events
        return all_events[n - 5: n]

class ShowPendingView(generic.ListView):
    template_name = "hoo_event/pending_event.html"
    context_object_name = "pending_events"

    def get_queryset(self):
        """
        get all pending events so admin can look at each and approve.
        """
        return Event.objects.filter(event_status__exact=EventStatus.PENDING)

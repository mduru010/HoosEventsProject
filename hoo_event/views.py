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
from .models import EventForm, Event, EventStatus, HeadCount
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
        return redirect(reverse("hoo_event:pending"))
    elif request.user.groups.filter(name='regular_users').exists():
        return redirect(reverse('hoo_event:index'))

def addEvent(request):
    form = EventForm()
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event_title = form.cleaned_data['event_title']
            event_street_address = form.cleaned_data['event_street_address']
            event_city = form.cleaned_data['event_city']
            event_state = form.cleaned_data['event_state']
            event_start_time = form.cleaned_data['event_start_time']
            event_end_time = form.cleaned_data['event_end_time']
            # event_description = form.cleaned_data['event_description']

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
                event_email = request.user.email,
                # event_description = event_description
            )

            new_event.save()
            return HttpResponseRedirect(reverse('hoo_event:index'))
        else:
            print(form.errors)

    return render(request, "hoo_event/create_event.html", {"form": form})

def event(request, event_id):
    current_event = get_object_or_404(Event, pk=event_id)
    events_signed_up = HeadCount.objects.filter(event__exact=current_event,
                                                user_email__exact=request.user.email)
    return render(request, 'event.html', {'event': current_event, 'events_signed_up': events_signed_up})

class ShowRecentView(generic.ListView):
    template_name = "hoo_event/recent_event.html"
    context_object_name = "latest_events"

    def get_queryset(self):
        """
        Get the most 5 recently added events
        """
        all_events = Event.objects.filter(event_status__exact=EventStatus.APPROVED).order_by("id").values()
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
        all_pending = Event.objects.filter(event_status__exact=EventStatus.PENDING).order_by("id").values()
        n = len(all_pending)
        if n < 10:
            return all_pending
        return all_pending[n - 10: n]

class ShowDeniedView(generic.ListView):
    template_name = "hoo_event/denied_event.html"
    context_object_name = "denied_events"

    def get_queryset(self):
        """
        get all pending events so admin can look at each and approve.
        """
        denied_events = Event.objects.filter(event_status__exact=EventStatus.DENIED).order_by("id").values()
        n = len(denied_events)

        if n < 10:
            return denied_events
        return denied_events[n - 10: n]


def approveEvent(request, event_id):
    current_event = get_object_or_404(Event, id=event_id)
    current_event.event_status = EventStatus.APPROVED
    current_event.save()
    return HttpResponseRedirect(reverse('hoo_event:index'))

def denyEvent(request, event_id):
    current_event = get_object_or_404(Event, id=event_id)
    current_event.event_status = EventStatus.DENIED
    current_event.save()
    return HttpResponseRedirect(reverse('hoo_event:index'))

def signUpEvent(request, event_id):
    current_event = get_object_or_404(Event, id=event_id)
    if current_event.event_capacity > 0:
        current_event.event_capacity -= 1
        current_event.save()

        new_head_count = HeadCount.objects.create(user_email=request.user.email, event=current_event)
        new_head_count.save()
        return HttpResponseRedirect(reverse('hoo_event:signUpSuccess', kwargs={'event_id' : event_id}))
    return HttpResponseRedirect(reverse('hoo_event:signUpFail', kwargs={'event_id' : event_id}))

def removeSignUpEvent(request, event_id):
    current_event = get_object_or_404(Event, id=event_id)
    current_event.event_capacity += 1
    current_event.save()

    current_head_count = get_object_or_404(HeadCount, user_email=request.user.email, event=current_event)
    current_head_count.delete()
    return HttpResponseRedirect(reverse('hoo_event:index'))

def showMyEvent(request):
    host_events = Event.objects.filter(event_email__exact=request.user.email,
                                       event_status__exact=EventStatus.APPROVED)
    # I learnt how to query foreign key from here:
    # https://stackoverflow.com/questions/15507171/django-filter-query-foreign-key
    joined_events = Event.objects.filter(headcount__user_email__exact=request.user.email)
    return render(request, 'my_event.html', {'host_events': host_events, 'joined_events': joined_events})
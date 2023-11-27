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
from .context_processors import user_group
import requests
from django.http import HttpResponseRedirect
from django.contrib.auth.models import Group, Permission
from django.urls import reverse
from django.utils import timezone
from django.views import generic
from django.core.serializers import serialize
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
        return redirect(reverse('hoo_event:home'))
    

def home(request):
    events = Event.objects.filter(event_status__exact=EventStatus.APPROVED)
    events = serialize('json', events)
    context = {'events': events}
    return render(request, 'hoo_event/home.html', context)

def addEvent(request):
    form = EventForm()
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event_title = form.cleaned_data['event_title']
            event_description = form.cleaned_data['event_description']
            event_capacity = form.cleaned_data['event_capacity']
            event_street_address = form.cleaned_data['event_street_address']
            event_city = form.cleaned_data['event_city']
            event_state = form.cleaned_data['event_state']
            event_start_time = form.cleaned_data['event_start_time']
            event_end_time = form.cleaned_data['event_end_time']

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
                event_description=event_description,
                event_latitude = lat,
                event_longitude = lng,
                event_street_address=event_street_address,
                event_city=event_city,
                event_state=event_state,
                event_start_time = event_start_time,
                event_end_time = event_end_time,
                event_status = EventStatus.PENDING,
                event_email = request.user.email,
                event_capacity=0,
                event_full_capacity=event_capacity
            )

            new_event.save()
            return HttpResponseRedirect(reverse('hoo_event:home'))
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
    paginate_by = 5
    model = Event  
    queryset = Event.objects.filter(event_status=EventStatus.APPROVED).order_by("-id")
    

class ShowPendingView(generic.ListView):
    template_name = "hoo_event/pending_event.html"
    context_object_name = "pending_events"
    paginate_by = 5  
    model = Event  

    # https://stackoverflow.com/questions/24725617/how-to-make-generic-listview-only-show-users-listing
    # This link helped me realized I can use self.request
    def get_queryset(self):
        user_email = self.request.user.email
        user_groups = user_group(self.request)
        if "admin_users" in user_groups["user_groups"]:
            return Event.objects.filter(event_status=EventStatus.PENDING).order_by("-id").values()
        else:
            return Event.objects.filter(event_status=EventStatus.PENDING,
                                        event_email=user_email).order_by("-id").values()

class ShowDeniedView(generic.ListView):
    template_name = "hoo_event/denied_event.html"
    context_object_name = "denied_events"
    paginate_by = 5  
    model = Event

    def get_queryset(self):
        user_email = self.request.user.email
        return Event.objects.filter(event_status=EventStatus.DENIED,
                                    event_email=user_email).order_by("-id").values()

def approveEvent(request, event_id):
    current_event = get_object_or_404(Event, id=event_id)
    current_event.event_status = EventStatus.APPROVED
    current_event.save()
    return HttpResponseRedirect(reverse('hoo_event:pending'))

def denyEvent(request, event_id):
    current_event = get_object_or_404(Event, id=event_id)
    current_event.event_status = EventStatus.DENIED
    current_event.save()
    return HttpResponseRedirect(reverse('hoo_event:pending'))

def signUpEvent(request, event_id):
    current_event = get_object_or_404(Event, id=event_id)
    if current_event.event_capacity < current_event.event_full_capacity and current_event.event_status == "EventStatus.APPROVED":
        current_event.event_capacity += 1
        current_event.save()

        new_head_count = HeadCount.objects.create(user_email=request.user.email, event=current_event)
        new_head_count.save()
        return HttpResponseRedirect(reverse('hoo_event:signUpSuccess', kwargs={'event_id' : event_id}))
    return HttpResponseRedirect(reverse('hoo_event:signUpFail', kwargs={'event_id' : event_id}))

def removeSignUpEvent(request, event_id):
    current_event = get_object_or_404(Event, id=event_id)
    current_event.event_capacity -= 1
    current_event.save()

    current_head_count = get_object_or_404(HeadCount, user_email=request.user.email, event=current_event)
    current_head_count.delete()
    return HttpResponseRedirect(reverse('hoo_event:home'))

def showMyEvent(request):
    host_events = Event.objects.filter(event_email__exact=request.user.email,
                                       event_status__exact=EventStatus.APPROVED)
    # I learnt how to query foreign key from here:
    # https://stackoverflow.com/questions/15507171/django-filter-query-foreign-key
    joined_events = Event.objects.filter(headcount__user_email__exact=request.user.email)
    return render(request, 'my_event.html', {'host_events': host_events, 'joined_events': joined_events})

def editEvent(request, event_id):
    current_event = get_object_or_404(Event, id=event_id)
    return render(request, 'edit_event.html', {'event': current_event})


def updateEvent(request, event_id):
    form = EventForm()
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event_title = form.cleaned_data['event_title']
            event_description = form.cleaned_data['event_description']
            event_street_address = form.cleaned_data['event_street_address']
            event_city = form.cleaned_data['event_city']
            event_state = form.cleaned_data['event_state']
            event_start_time = form.cleaned_data['event_start_time']
            event_end_time = form.cleaned_data['event_end_time']

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

            current_event = get_object_or_404(Event, id=event_id)
            current_event.event_title = event_title
            current_event.event_description = event_description
            current_event.event_latitude = lat
            current_event.event_longitude = lng
            current_event.event_street_address = event_street_address
            current_event.event_city = event_city
            current_event.event_state = event_state
            current_event.event_start_time = event_start_time
            current_event.event_end_time = event_end_time

            current_event.save()
            return HttpResponseRedirect(reverse('hoo_event:event', kwargs={'event_id' : event_id}))
        else:
            print(form.errors)

    return render(request, "hoo_event/edit_event.html", {"form": form})

def deleteEvent(request, event_id):
    current_event = get_object_or_404(Event, id=event_id)
    current_event.delete()
    return HttpResponseRedirect(reverse('hoo_event:home'))



















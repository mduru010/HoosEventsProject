import unittest
from django.urls import reverse
from .models import Event, EventForm, EventStatus
from django.contrib.auth.models import User, Group
from .views import addEvent
from django.test import Client, TestCase
import time
from datetime import datetime
from django.utils import timezone

class EventModelTest(unittest.TestCase):

    event_data = {
        'event_title': "Test Event",
        'event_latitude': 40.7128,
        'event_longitude': -74.0060,
        'event_street_address': "123 Main St",
        'event_city': "New York",
        'event_state': "NY",
    }
    def test_create_event(self):
        # Create a test event
        event = Event()
        event.event_title = "Test Event"
        event.event_latitude = 40.7128
        event.event_longitude = -74.0060
        event.event_street_address = "123 Main St"
        event.event_city = "New York"
        event.event_state = "NY"


        self.assertEqual(event.event_title, self.event_data['event_title'])
        self.assertEqual(event.event_latitude, self.event_data['event_latitude'])
        self.assertEqual(event.event_longitude, self.event_data['event_longitude'])
        self.assertEqual(event.event_street_address, self.event_data['event_street_address'])
        self.assertEqual(event.event_city, self.event_data['event_city'])
        self.assertEqual(event.event_state, self.event_data['event_state'])

    def test_event_model_string_representation(self):
        event = Event()
        event.event_title = "Test Event"
        event.event_latitude = 40.7128
        event.event_longitude = -74.0060
        event.event_street_address = "123 Main St"
        event.event_city = "New York"
        event.event_state = "NY"
        # Check if the string representation of the event is as expected
        self.assertEqual(str(event), self.event_data['event_title'])

##################

    def test_event_creation(self):
        # Test creating an event using the view
        client = Client()
        user = User.objects.create_user(
            username=f"unique_testuser_{int(time.time())}",
            password="testpassword",
        )
        client.login(username=user.username, password="testpassword")

        # Define start and end times in a valid format (replace with actual date and time)
        start_time = timezone.make_aware(datetime(2023, 11, 1, 10, 0, 0))
        end_time = timezone.make_aware(datetime(2023, 11, 1, 12, 0, 0))

        event_data = {
            'event_title': 'test_event_creation',
            'event_street_address': '456 Elm St',
            'event_city': 'Los Angeles',
            'event_state': 'CA',
            'event_start_time': start_time,  # Use valid date and time
            'event_end_time': end_time,  # Use valid date and time
        }

        response = client.post(reverse('hoo_event:addNewEvent'), event_data)
        self.assertEqual(response.status_code, 302)  # Check for a redirect (status code 302)

        # Get all events with the title 'test_event_creation'
        events = Event.objects.filter(event_title='test_event_creation')

        # Check if at least one event with the given title exists
        self.assertTrue(events.exists())

        # You can also check other attributes of the events
        for new_event in events:
            self.assertEqual(new_event.event_title, event_data['event_title'])
            self.assertEqual(new_event.event_street_address, event_data['event_street_address'])
            self.assertEqual(new_event.event_city, event_data['event_city'])
            self.assertEqual(new_event.event_state, event_data['event_state'])
            self.assertEqual(new_event.event_status, str(EventStatus.PENDING))  # Check that the event status is pending
            self.assertEqual(new_event.event_start_time, start_time)  # Check event start time
            self.assertEqual(new_event.event_end_time, end_time)  # Check event end time

    def test_event_detail_view(self):
        event = Event.objects.create(
            event_title="Test Event",
            event_latitude=40.7128,
            event_longitude=-74.0060,
            event_street_address="123 Main St",
            event_city="New York",
            event_state="NY",
        )
        client = Client()
        response = client.get(reverse('hoo_event:event', args=[event.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Test Event" in response.content.decode())

    def test_recent_events_view(self):
        # Create a test event with the event status set to approved
        event = Event.objects.create(
            event_title="Test Event",
            event_latitude=40.7128,
            event_longitude=-74.0060,
            event_street_address="123 Main St",
            event_city="New York",
            event_state="NY",
            event_status=EventStatus.APPROVED,  # Set the event status to approved
        )

        client = Client()
        response = client.get(reverse('hoo_event:recent'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Test Event" in response.content.decode())
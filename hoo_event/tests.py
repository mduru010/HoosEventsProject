import unittest
from django.urls import reverse
from .models import Event, EventForm, EventStatus
from django.contrib.auth.models import User, Group
from .views import addEvent
from django.test import Client, TestCase
import time

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

    # def test_event_creation(self):
    #     # Test creating an event using the view
    #     client = Client()
    #     user = User.objects.create_user(
    #         username=f"unique_testuser_{int(time.time())}",
    #         password="testpassword",
    #     )
    #     client.login(username=user.username, password="testpassword")
    #
    #     event_data = {
    #         'event_title': 'test_event_creation',
    #         'event_street_address': '456 Elm St',
    #         'event_city': 'Los Angeles',
    #         'event_state': 'CA',
    #     }
    #
    #     response = client.post(reverse('hoo_event:addNewEvent'), event_data)
    #     self.assertEqual(response.status_code, 200)  # Check for successful redirect after form submission
    #
    #     # Get all events with the title 'New Test Event'
    #     events = Event.objects.filter(event_title__exact='test_event_creation')
    #     print(events)
    #     # Check if at least one event with the given title exists
    #     self.assertTrue(events.exists())
    #
    #     # You can also check other attributes of the events if needed
    #     for new_event in events:
    #         self.assertEqual(new_event.event_title, event_data['event_title'])
    #         self.assertEqual(new_event.event_street_address, event_data['event_street_address'])
    #         self.assertEqual(new_event.event_city, event_data['event_city'])
    #         self.assertEqual(new_event.event_state, event_data['event_state'])
    #         self.assertEqual(new_event.event_status, EventStatus.PENDING)  # Check that the event is approved

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

    # def test_recent_events_view(self):
    #     # Create a test event with the approved field set to True
    #     event = Event.objects.create(
    #         event_title="Test Event",
    #         event_latitude=40.7128,
    #         event_longitude=-74.0060,
    #         event_street_address="123 Main St",
    #         event_city="New York",
    #         event_state="NY",
    #         approved=True,  # Set the approved field to True
    #     )
    #     client = Client()
    #     response = client.get(reverse('hoo_event:recent'))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTrue("Test Event" in response.content.decode())
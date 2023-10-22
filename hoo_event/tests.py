from django.test import TestCase
import unittest
from django.urls import reverse
from .models import Event, EventForm
from django.contrib.auth.models import User, Group
from .views import addEvent
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
    def tearDown(self):
        # Clean up the database
        self.user.delete()
    def setUp(self):
        # Create a test user with a unique username
        self.user = User.objects.create_user(
            username=f"unique_testuser_{int(time.time())}",  # Append a timestamp
            password="testpassword",
        )
        # Set up the test client
        self.client = Client()

    def test_add_event_view_accessible_by_logged_in_user(self):
        self.client.login(username=self.user.username, password="testpassword")
        response = self.client.get(reverse('addNewEvent'))
        self.assertEqual(response.status_code, 200)

    def test_add_event_view_redirects_to_login_for_anonymous_user(self):
        response = self.client.get(reverse('addNewEvent'))
        self.assertRedirects(response, reverse('login') + f'?next={reverse("addNewEvent")}')

    def test_event_detail_view(self):
        event = Event.objects.create(
            event_title="Test Event",
            event_latitude=40.7128,
            event_longitude=-74.0060,
            event_street_address="123 Main St",
            event_city="New York",
            event_state="NY",
        )
        response = self.client.get(reverse('event', args=[event.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Event")

    def test_recent_events_view(self):
        response = self.client.get(reverse('recent_events'))
        self.assertEqual(response.status_code, 200)
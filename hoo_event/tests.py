from django.test import TestCase
import unittest
from django.urls import reverse
from .models import Event, EventForm
from django.contrib.auth.models import User, Group
from .views import addEvent

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

        # event = Event.objects.create(**event_data)
        # event_data = {
        #     'event_title': "Test Event",
        #     'event_latitude': 40.7128,
        #     'event_longitude': -74.0060,
        #     'event_street_address': "123 Main St",
        #     'event_city': "New York",
        #     'event_state': "NY",
        # }

        # Check if the event was created successfully
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
    # def test_add_event_view_accessible_by_logged_in_user(self):
    #     self.client.login(username="testuser", password="testpassword")
    #     response = self.client.get(reverse('addNewEvent'))

    #     # Check if the response status code is 200 (OK)
    #     self.assertEqual(response.status_code, 200)


    # def test_add_event_view_redirects_to_login_for_anonymous_user(self):
    #     response = self.client.get(reverse('addNewEvent'))

    #     # Check if the response redirects to the login page
    #     self.assertRedirects(response, reverse('login') + f'?next={reverse("addNewEvent")}')

    def test_create_event(self):
        user = User.objects.create_user(
            username="testuser",
            password="testpassword",
        )
        self.client.login(username="testuser", password="testpassword")

        event_data = {
            'event_title': 'Test Event',
            'event_latitude': 40.7128,
            'event_longitude': -74.0060,
            'event_street_address': '123 Main St',
            'event_city': 'New York',
            'event_state': 'NY',
        }

        response = self.client.post(reverse('addNewEvent'), event_data)
        self.assertRedirects(response, reverse('hoo_event:index'))
        self.assertTrue(Event.objects.filter(event_title=event_data['event_title']).exists())
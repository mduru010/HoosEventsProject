from django.test import TestCase
from django.urls import reverse
from .models import Event, EventForm
from django.contrib.auth.models import User, Group

class EventModelTest(TestCase):
    def test_create_event(self):
        event_data = {
            'event_title': "Test Event",
            'event_latitude': 40.7128,
            'event_longitude': -74.0060,
            'event_street_address': "123 Main St",
            'event_city': "New York",
            'event_state': "NY",
        }

        # Create a test event
        event = Event.objects.create(**event_data)

        # Check if the event was created successfully
        self.assertEqual(event.event_title, event_data['event_title'])
        self.assertEqual(event.event_latitude, event_data['event_latitude'])
        self.assertEqual(event.event_longitude, event_data['event_longitude'])
        self.assertEqual(event.event_street_address, event_data['event_street_address'])
        self.assertEqual(event.event_city, event_data['event_city'])
        self.assertEqual(event.event_state, event_data['event_state'])

    def test_event_model_string_representation(self):
        event_data = {
            'event_title': "Test Event",
            'event_latitude': 40.7128,
            'event_longitude': -74.0060,
            'event_street_address': "123 Main St",
            'event_city': "New York",
            'event_state': "NY",
        }

        event = Event.objects.create(**event_data)

        # Check if the string representation of the event is as expected
        self.assertEqual(str(event), event_data['event_title'])

class AddEventViewTest(TestCase):
    def setUp(self):
        # Create a regular user
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword",
        )

    def test_add_event_view_accessible_by_logged_in_user(self):
        # Log in the user
        self.client.login(username="testuser", password="testpassword")

        # Access the add event view
        response = self.client.get(reverse('add_event'))

        # Check if the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

    def test_add_event_view_redirects_to_login_for_anonymous_user(self):
        # Access the add event view without logging in
        response = self.client.get(reverse('add_event'))

        # Check if the response redirects to the login page
        self.assertRedirects(response, reverse('login') + f'?next={reverse("add_event")}')

    def test_create_event(self):
        # Log in the user
        self.client.login(username="testuser", password="testpassword")

        event_data = {
            'event_title': 'Test Event',
            'event_latitude': 40.7128,
            'event_longitude': -74.0060,
            'event_street_address': '123 Main St',
            'event_city': 'New York',
            'event_state': 'NY',
        }

        # Create a test event
        response = self.client.post(reverse('add_event'), event_data)

        # Check if the response redirects to the event list page after creating an event
        self.assertRedirects(response, reverse('event_list'))

        # Check if the event was created in the database
        self.assertTrue(Event.objects.filter(event_title=event_data['event_title']).exists())

    def test_invalid_event_form_submission(self):
        # Log in the user
        self.client.login(username="testuser", password="testpassword")

        # Submit an invalid event form with missing data
        response = self.client.post(reverse('add_event'), {
            'event_title': '',  # Missing event title
        })

        # Check if the form submission displays errors
        self.assertFormError(response, 'form', 'event_title', 'This field is required.')

    def test_event_detail_view(self):
        event_data = {
            'event_title': "Test Event",
            'event_latitude': 40.7128,
            'event_longitude': -74.0060,
            'event_street_address': "123 Main St",
            'event_city': "New York",
            'event_state': "NY",
        }

        # Create a test event
        event = Event.objects.create(**event_data)

        # Access the event detail view
        response = self.client.get(reverse('event_detail', args=[event.id]))

        # Check if the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check if the event's title is displayed in the response content
        self.assertContains(response, event_data['event_title'])

# Create your tests here.

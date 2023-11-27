import unittest
from django.urls import reverse
from django.shortcuts import get_object_or_404
from .models import Event, EventForm, EventStatus
from django.contrib.auth.models import User, Group
from .views import addEvent
from django.test import Client, TestCase
import time, random
from datetime import datetime
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User, Group, Permission
from .models import Event, EventStatus

class EventModelTest(unittest.TestCase):
    # event_start_time = models.DateTimeField(default=timezone.now)  # Use timezone.now()
    # event_end_time = models.DateTimeField(default=timezone.now)  # Use timezone.now()

    # event_status = models.CharField(default=EventStatus.PENDING, max_length=10)

    event_data = {
        'event_title': "Test Event",
        'event_latitude': 40.7128,
        'event_longitude': -74.0060,
        'event_street_address': "123 Main St",
        'event_city': "New York",
        'event_state': "NY",
    }

    def tearDown(self):
        Event.objects.filter(event_title__exact='Test Event').delete()  # Delete the test event

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
            'event_description': 'Welcome',
            'event_capacity': 10,
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

        Event.objects.filter(event_title__exact='test_event_creation').delete() # Delete the test event

    def test_event_detail_view(self):
        client = Client()
        user = User.objects.create_user(
            username=f"unique_testuser_{int(time.time())}",
            password="testpassword",
        )
        client.login(username=user.username, password="testpassword")

        current_event = get_object_or_404(Event, id=450)
        response = client.get(reverse('hoo_event:event', args=[current_event.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(current_event.event_title in response.content.decode())

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

class AdminUserTests(unittest.TestCase):
    def setUp(self):
        # Create a regular user with a unique username
        regular_username = f"unique_testuser_{int(time.time())}"
        self.regular_user = User.objects.create_user(
            username=regular_username + str(random.randrange(20000)),
            password='regularpassword'
        )

        # Create an admin user with a unique username
        admin_username = f"unique_adminuser_{int(time.time())}"
        self.admin_user = User.objects.create_user(
            username=admin_username + str(random.randrange(20000)),
            password='adminpassword'
        )

        # Create an Event
        self.event = Event.objects.create(
            event_title="Test Event",
            event_longitude=40.7128,
            event_latitude=-74.0060,
            event_street_address="123 Main St",
            event_city="New York",
            event_state="NY",
            event_status=EventStatus.PENDING
        )

        # Add the admin user to the admin_users group
        admin_users_group, created = Group.objects.get_or_create(name='admin_users')
        self.admin_user.groups.add(admin_users_group)

        # Create a test client
        self.client = Client()

    def tearDown(self):
        Event.objects.filter(event_title__exact=self.event).delete()  # Delete the test event

    def test_admin_can_approve_event(self):
        # Create a test client
        client = Client()

        # Admin user logs in
        client.login(username='adminuser', password='adminpassword')

        # Get the event detail page
        response = client.get(reverse('hoo_event:event', args=[self.event.id]))

        # Check that the response status code is 200 (success)
        self.assertEqual(response.status_code, 200)

        # Check that the "Approve" button is present on the page
        self.assertIn('Approve', response.content.decode())

        # Simulate approving the event by posting the approval form (you need to define this in your app)
        response = client.post(reverse('hoo_event:approveEvent', args=[self.event.id]))

        # Refresh the event from the database
        self.event.refresh_from_db()

        # Check that the event status is now "APPROVED" using the integer value
        self.assertEqual(self.event.event_status, "EventStatus.APPROVED")

    def test_regular_user_cannot_approve_event(self):
        # Create a test client
        client = Client()

        # Regular user logs in
        client.login(username='regularuser', password='regularpassword')

        # Get the event detail page
        response = client.get(reverse('hoo_event:event', args=[self.event.id]))

        # Check the response status code
        self.assertEqual(response.status_code, 200)

        # Check if the "Approve" button is not present by looking for its attributes
        self.assertNotIn('<input type="submit" value="APPROVED">', response.content.decode())

    def test_admin_can_deny_event(self):
        # Admin user logs in
        self.client.login(username=self.admin_user.username, password='adminpassword')

        # Get the event detail page
        response = self.client.get(reverse('hoo_event:event', args=[self.event.id]))

        # Check that the "Deny" button is present on the page
        self.assertIn('Deny', response.content.decode())

        # Simulate denying the event by posting the denial form
        response = self.client.post(reverse('hoo_event:denyEvent', args=[self.event.id]))

        # Check that the event status is now "DENIED"
        self.event.refresh_from_db()
        self.assertEqual(self.event.event_status, "EventStatus.DENIED")

    def test_delete_all_test_events(self):
        Event.objects.filter(event_title="Test Event").delete()
        Event.objects.filter(event_title="test_event_creation").delete()


class SignUpTest(unittest.TestCase):
    def setUp(self):
        self.regular_username = f"unique_regular_user_{int(time.time())}{random.randrange(20000)}"
        self.regular_user = User.objects.create_user(
            username=self.regular_username,
            password='regular_password'
        )

        # Create an admin user with a unique username
        self.admin_username = f"unique_admin_user_{int(time.time())}{random.randrange(20000)}"
        self.admin_user = User.objects.create_user(
            username=self.admin_username,
            password='admin_password'
        )
        admin_users_group, created = Group.objects.get_or_create(name='admin_users')
        self.admin_user.groups.add(admin_users_group)

        event_title = f"Hoos Hack {int(time.time())}"
        year = 2023
        month = 12
        day = 10
        hours = 12
        minutes = 10

        self.new_event = {"event_title": event_title,
                     "event_capacity": 1,
                     "event_description": "Welcome!",
                     "event_start_time": datetime(year, month, day, hours, minutes),
                     "event_end_time": datetime(year, month, day, hours, minutes+1),
                     "event_street_address": "85 Engineer's Way",
                     "event_city": "Charlottesville",
                     "event_state": "Virginia"}

    def tearDown(self):
        # delete the created users
        User.objects.filter(username__exact=self.regular_username).delete()
        User.objects.filter(username__exact=self.admin_username).delete()

        Event.objects.filter(event_title__exact=self.new_event["event_title"]).delete()

    def test_sign_up_success(self):

        client = Client()
        client.login(username=self.admin_user.username, password='admin_password')

        response = client.post(reverse("hoo_event:addNewEvent"), self.new_event)
        self.assertEqual(response.status_code, 302)

        # check if this event correctly appears in pending
        response = client.get(reverse('hoo_event:pending'))
        self.assertIn(self.new_event["event_title"], response.content.decode())

        # get the event id and approve it
        event_id = Event.objects.get(event_title=self.new_event["event_title"]).id
        response = client.post(reverse('hoo_event:approveEvent',  kwargs={'event_id' : event_id}))
        self.assertEqual(response.status_code, 302)

        # sign up
        response = client.get(reverse('hoo_event:event', kwargs={'event_id': event_id}))
        self.assertIn('Sign Up', response.content.decode())

        response = client.post(reverse('hoo_event:signUp', kwargs={'event_id': event_id}))
        self.assertEqual(response.status_code, 302)
        self.assertIn(f'/hoo_event/event/{event_id}/register/success', str(response))

        # check that the signed up event got added to our list
        response = client.get(reverse('hoo_event:myEvents'))
        self.assertIn(self.new_event["event_title"], response.content.decode())

    def test_sign_up_fail(self):

        client = Client()
        client2 = Client()
        client.login(username=self.admin_user.username, password='admin_password')
        client2.login(username=self.regular_user.username, password='regular_password')

        # admin (client) creates the event
        response = client.post(reverse("hoo_event:addNewEvent"), self.new_event)
        self.assertEqual(response.status_code, 302)

        # get the event id and approve it
        event_id = Event.objects.get(event_title=self.new_event["event_title"]).id
        response = client.post(reverse('hoo_event:approveEvent', kwargs={'event_id': event_id}))
        self.assertEqual(response.status_code, 302)

        # admin signs up
        response = client.post(reverse('hoo_event:signUp', kwargs={'event_id': event_id}))
        self.assertEqual(response.status_code, 302)
        self.assertIn(f'/hoo_event/event/{event_id}/register/success', str(response))

        # regular user (client2) signs up fail now as capacity has been reached
        response = client2.post(reverse('hoo_event:signUp', kwargs={'event_id': event_id}))
        self.assertEqual(response.status_code, 302)
        self.assertIn(f'/hoo_event/event/{event_id}/register/fail', str(response))

    def test_sign_up_pending(self):
        client = Client()
        client.login(username=self.admin_user.username, password='admin_password')

        # admin (client) creates the event
        response = client.post(reverse("hoo_event:addNewEvent"), self.new_event)
        self.assertEqual(response.status_code, 302)

        # get the event id
        event_id = Event.objects.get(event_title=self.new_event["event_title"]).id

        # sign up without approving
        response = client.post(reverse('hoo_event:signUp', kwargs={'event_id': event_id}))
        self.assertEqual(response.status_code, 302)
        self.assertIn(f'/hoo_event/event/{event_id}/register/fail', str(response))
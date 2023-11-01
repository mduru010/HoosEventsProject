from django.contrib import admin
from .models import Event
# Register your models here.
from django.contrib.auth.models import Group, Permission

regular_users, created = Group.objects.get_or_create(name ='regular_users')
admin_users, created = Group.objects.get_or_create(name ='admin_users')

# def approve_events(modeladmin, request, queryset):
#     # Mark selected events as approved
#     queryset.update(approved=True)

# approve_events.short_description = "Approve selected events"

# class EventAdmin(admin.ModelAdmin):
#     list_display = ('event_title', 'approved', 'event_street_address', 'event_city', 'event_state')
#     actions = [approve_events]

# admin.site.register(Event, EventAdmin)
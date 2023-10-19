from django.urls import path
from . import views
from django.views.generic import TemplateView

app_name = "hoo_event"
urlpatterns = [
    path('event/<int:event_id>/', views.event, name='event'),
    path('', TemplateView.as_view(template_name="index.html"), name="index"),
    path('add/', views.addEvent, name="addNewEvent"),
]
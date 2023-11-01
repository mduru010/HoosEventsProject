from django.urls import path
from . import views
from django.views.generic import TemplateView
from django.contrib import admin
from django.urls import include, path

app_name = "hoo_event"
urlpatterns = [
    path('event/<int:event_id>/', views.event, name='event'),
    path('', TemplateView.as_view(template_name="index.html"), name="index"),
    path('add/', views.addEvent, name="addNewEvent"),
    path('recent/', views.ShowRecentView.as_view(), name="recent"),
    path('pending/', views.ShowPendingView.as_view(), name="pending"),
    path('denied/', views.ShowDeniedView.as_view(), name="denied"),
    path('event/<int:event_id>/approve', views.approveEvent, name="approveEvent"),
    path('event/<int:event_id>/deny', views.denyEvent, name="denyEvent"),
]
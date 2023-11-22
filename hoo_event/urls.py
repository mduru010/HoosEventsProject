from django.urls import path
from . import views
from django.views.generic import TemplateView
from django.contrib import admin
from django.urls import include, path

app_name = "hoo_event"
urlpatterns = [
    path('event/<int:event_id>/', views.event, name='event'),
    path('', TemplateView.as_view(template_name="index.html"), name="index"),
    path('home/', views.home, name="home"),
    path('add/', views.addEvent, name="addNewEvent"),
    path('my_event/', views.showMyEvent, name="myEvents"),
    path('recent/', views.ShowRecentView.as_view(), name="recent"),
    path('pending/', views.ShowPendingView.as_view(), name="pending"),
    path('denied/', views.ShowDeniedView.as_view(), name="denied"),
    path('event/<int:event_id>/approve', views.approveEvent, name="approveEvent"),
    path('event/<int:event_id>/deny', views.denyEvent, name="denyEvent"),
    path('event/<int:event_id>/register', views.signUpEvent, name="signUp"),
    path('event/<int:event_id>/deregister', views.removeSignUpEvent, name="removeSignUp"),
    path('event/<int:event_id>/register/success', TemplateView.as_view(template_name="sign_up_success.html"), name="signUpSuccess"),
    path('event/<int:event_id>/register/fail', TemplateView.as_view(template_name="sign_up_fail.html"), name="signUpFail"),
    path('event/<int:event_id>/edit', views.editEvent, name="editEvent"),
    path('event/<int:event_id>/update', views.updateEvent, name="updateEvent"),
    path('event/<int:event_id>/delete', views.deleteEvent, name="deleteEvent"),
    path('googled45417b2986febe5.html/', TemplateView.as_view(template_name="googled45417b2986febe5.html"), name="g-verification"),
]
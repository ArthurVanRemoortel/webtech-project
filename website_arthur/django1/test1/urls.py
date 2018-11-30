from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('venues', views.venues, name='venues'),
    path('add_venue_form_test', views.add_venue_form_test, name='add_venue_form_test'),
    path('add_event_form_test', views.add_event_form_test, name='add_event_form_test'),

    path('events/', views.event_page, name='event_page'),
]
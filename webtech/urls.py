from django.urls import path, include, re_path
from rest_framework import routers
from . import views, api_views


urlpatterns = [
    path('', views.index, name='index'),
    path('map', views.map, name='map'),
    path('bookmark_event/<int:event_id>', views.bookmark_event, name='bookmark_event'),
    path('bookmark_venue/<int:venue_id>', views.bookmark_venue, name='bookmark_venue'),
    path('add_venue_form_test', views.add_venue_form_test, name='add_venue_form_test'),
    path('add_event_form_test', views.add_event_form_test, name='add_event_form_test'),

    path('events/<int:event_id>', views.event_page, name='event_page'),
    path('venues/<int:venue_id>', views.venue_page, name='venue_page'),

    # API
    path('api/events/', api_views.event_list),
    path('api/events/<int:pk>/', api_views.event_detail),

    path('api/venues/', api_views.venue_list),
    path('api/venues/<int:pk>/', api_views.venue_detail),

    path('api/reviews/<int:venue_id>/', api_views.reviews),

    # Testing only
    path('scrapelastfm/', views.scrapelastfm, name='scrapelastfm'),
    path('scrape/', views.scrape, name='scrape')


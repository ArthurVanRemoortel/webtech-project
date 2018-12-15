from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('map', views.map, name='map'),
    path('bookmark_event/<int:event_id>', views.bookmark_event, name='bookmark_event'),
    path('add_venue_form_test', views.add_venue_form_test, name='add_venue_form_test'),
    path('add_event_form_test', views.add_event_form_test, name='add_event_form_test'),

    path('events/<int:event_id>', views.event_page, name='event_page'),
    path('venues/<int:venue_id>', views.venue_page, name='venue_page'),

    path('scrape/', views.scrape, name='scrape'),
    path('scrapelastfm/', views.scrapelastfm, name='scrapelastfm'),

]

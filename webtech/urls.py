from django.urls import path, include, re_path
from . import views, api_views


urlpatterns = [
    path('', views.index, name='index'),

    path('map/', views.map, name='map'),
    path('map/<int:event_id>/', views.map, name='event_map'),
    path('user_locate/', views.user_locate, name='user_locate'),
    path('events_on_date/', views.events_on_date, name='events_on_date'),

    path('bookmark_event/<int:event_id>', views.bookmark_event, name='bookmark_event'),
    path('bookmark_venue/<int:venue_id>', views.bookmark_venue, name='bookmark_venue'),

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
    path('scrape/', views.scrape, name='scrape'),
]

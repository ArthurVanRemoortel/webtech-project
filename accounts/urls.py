from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
	path('', views.home),
	path('login/', LoginView.as_view(template_name='accounts/login.html'), name='login'),
	path('logout/', LogoutView.as_view(template_name='accounts/login.html'), name='logout'),
	path('profile/', views.profile, name='profile'),
	path('register/', views.register, name='register'),
	# path('create/', views.VenueCreateView.as_view(), name='create_venue_review'),
]
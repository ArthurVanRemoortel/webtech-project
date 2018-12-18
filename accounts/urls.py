from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordResetView

urlpatterns = [
	path('', views.home),
	path('login/', LoginView.as_view(template_name='accounts/login.html'), name='login'),
	path('logout/', LogoutView.as_view(template_name='accounts/login.html'), name='logout'),
	path('profile/', views.Profile.as_view(), name='profile'),
	path('register/', views.register, name='register'),
	path('change-password/', PasswordChangeView.as_view(template_name='accounts/pw_change_form.html'), name='pw_change'),
	path('reset-password/', PasswordResetView.as_view(template_name='accounts/pw_reset_form.html'), name='pw-reset'),
]
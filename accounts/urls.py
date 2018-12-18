from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView, PasswordResetView

urlpatterns = [
	path('', views.home),
	path('login/', LoginView.as_view(template_name='accounts/login.html'), name='login'),
	path('logout/', LogoutView.as_view(template_name='accounts/login.html'), name='logout'),
	path('profile/', views.Profile.as_view(), name='profile'),
	path('register/', views.register, name='register'),
	path('password_change/', PasswordChangeView.as_view(template_name='accounts/pw_change_form.html'), name='pw_change'),
	# path('password_change/done', )
	path('password_reset/', PasswordResetView.as_view(template_name='accounts/pw_reset_form.html'), name='pw-reset'),
	path('password_reset/done', PasswordChangeDoneView.as_view(template_name='accounts/profile.html'), name='password_reset_confirm'),
]
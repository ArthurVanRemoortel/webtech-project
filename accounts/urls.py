from . import views
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
	path('', views.home, name='accounts_index'),
    path('profile/', views.Profile.as_view(),name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name="login"),
    path('logout/', auth_views.LogoutView.as_view(next_page='../login'),name="logout"),
    path('register/', views.register, name='register'),

    path('password_reset/', 		auth_views.PasswordResetView.as_view(template_name='password_reset_form.html') ,name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html') ,name='password_reset_done'),
    path('password_reset/confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html') ,name='password_reset_confirm'),
    path('password_reset/complete', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),

   	path('password_change/', 	auth_views.PasswordChangeView.as_view(template_name='password_change.html') ,name='password_change'),
   	path('password_change/done/',auth_views.PasswordChangeDoneView.as_view(template_name='password_change_done.html') ,name='password_change_done'),
   	# path('', include('django.contrib.auth.urls')),
]
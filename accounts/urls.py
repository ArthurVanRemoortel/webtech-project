from . import views
from django.urls import path
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('profile/', views.Profile.as_view(),name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name="login"),
    path('logout/', auth_views.LogoutView.as_view(next_page='../login'),name="logout"),
    path('register/', views.register, name='register'),

]
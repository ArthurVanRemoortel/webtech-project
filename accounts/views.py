from django.shortcuts import render

# Create your views here.

def home(request):
	current_user = request.user
	if current_user.is_authenticated:
		return redirect('/accounts/profile')
	else:
		return redirect('/accounts/login')
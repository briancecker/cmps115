from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm

# SHOW USER
def show_user(request, username="None"):
	if username is not "None":
		user_instance = get_object_or_404(User,  username=username)
	else:
		if not request.user.is_authenticated:
			return render(request, "user/user_page.html", {})
		else:
			user_instance = request.user

	context = {
			"user_instance" : user_instance,
		}
	return render(request, "user/user_page.html", context)

# CREATE USER
def create_user(request):
	form = SignUpForm()
	context = {
		"form": form,
	}
	return render(request, "user/signup.html", context)

# RETREIVE USER
def login_user(request):
	return HttpResponse("Login User")

# UPDATE USER
@login_required
def update_user(request):
	return HttpResponse("Update User")

# DELETE USER
@login_required
def delete_user(request):
	return HttpResponse("Delete User")

# LOGOFF USER
@login_required
def logoff_user(request):
	return HttpResponse("Logoff User")



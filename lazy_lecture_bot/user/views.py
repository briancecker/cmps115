from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm

#############
# SHOW USER #
#############
def show_user(request, username="None"):
	if username is not "None":
		user_instance = get_object_or_404(User,  username=username)
	else:
		if request.user.is_active: # ----------------------------- FIX THIS
			user_instance = request.user
		else:
			return redirect("login")

	context = {
			"user_instance" : user_instance,
		}
	return render(request, "user/user_page.html", context)

###################
# CREATE NEW USER #
###################
def signup_view(request):
	form = SignUpForm()
	context = {
		"form": form,
	}
	return render(request, "user/signup.html", context)

##############
# LOGIN USER #
##############
def login_user(request):
	if not request.user.is_authenticated:
		return render(request, "user/login.html", {})
	else:
		return redirect("/u/")

def auth_login(request): ## This is where the actual authentication is happening
	username = request.POST['username']
	password = request.POST['password']
	user = authenticate(username=username, password=password)
	if user is not None:
		if user.is_active:
			login(request, user)
			return redirect("/")
			# SUCCESS
		else:
			return HttpResponse("DISABLED :(") ## --------------------------FIX THIS
			# Redirect Disabled account
	else:
		# Return Invalid Login
		return HttpResponse("Invalid Login :(") ## ---------------------------FIX THIS

##########################################################
# UPDATE USER - Allows User to update their profile info #
##########################################################
@login_required
def update_user(request):
	return HttpResponse("Update User")


######################################################################################
# DELETE USER PROFILE - Doesn't actually delete the profile but marks it as inactive #
######################################################################################
@login_required
def delete_user(request):
	return HttpResponse("Delete User")


#############
#  LOGOFF   #
#############
@login_required
def logoff_user(request):
	logout(request)
	return redirect("/")



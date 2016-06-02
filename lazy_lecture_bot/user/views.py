from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from user.forms import *
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages

from videoapp.models import VideoPost

"""""""""""""""""

  	SHOW USER

"""""""""""""""""
def show_user(request, username="None"):
	if username is not "None":
		user_instance = get_object_or_404(User,  username=username)
		user_posts = VideoPost.objects.filter(public_access=True, author=user_instance).order_by('publish_date')
	else:
		if request.user.is_active:
			user_instance = request.user
		else:
			return redirect("login")

	context = {
			"vp" : user_posts,
			"user_instance" : user_instance,
		}

	return render(request, "user/user_page.html", context)

"""""""""""""""""""""

  	CREATE NEW USER / REGISTRATION

"""""""""""""""""""""
@csrf_protect
def signup_view(request):
	if request.method == "POST":
		form = RegistrationForm(request.POST)
		if form.is_valid():
			user = User.objects.create_user(
				username = form.cleaned_data['username'],
				password = form.cleaned_data['password'],
				email=form.cleaned_data['email']
				)
			user = authenticate(username=request.POST["username"], password=request.POST["password"])
			login(request, user)
			return redirect("/")
	else:
		form = RegistrationForm()

	context = {
		'form': form
	}
	return render(request, "user/signup.html", context)


"""""""""""""""

  	LOGIN USER

"""""""""""""""
def login_user(request):
	if not request.user.is_active:
		if request.method == "POST":
			form = LoginForm(request.POST)
			if form.is_valid():
				user = form.login(request)
				login(request, user)
				messages.add_message(request, messages.SUCCESS, 'Successfully Logged In! :D')
				return redirect("/")
			else:
				messages.add_message(request, messages.ERROR, 'Invalid Username/Password Combination :(', 'danger')
	else:
		return redirect(show_user)
	form = LoginForm()
	context = {
		'form': form
	}
	return render(request, "user/login.html", context)

def auth_login(request): ## This is where the actual authentication is happening
	if request.method == "POST":
		form = LoginForm(request.POST)
		redirect_to = request.GET.get("redirect")
		if form.is_valid():
			user = form.login(request)
			login(request, user)
			messages.add_message(request, messages.SUCCESS, 'Successfully Logged In! :D')
		else:
			messages.add_message(request, messages.ERROR, 'Invalid Username/Password Combination :(', 'danger')
		return redirect(redirect_to)

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

  	********** TBI *********
  	UPDATE USER - Allows User to update their profile info. 


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
@login_required
def update_user(request):
	return HttpResponse("Update User")


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

	******* TBI ************
  	DELETE USER PROFILE - Doesn't actually delete the profile but marks it as inactive


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
@login_required
def delete_user(request):
	return HttpResponse("Delete User")

"""""""""""""""

  	LOGOFF   

"""""""""""""""
@login_required
def logoff_user(request):
	redirect_to = request.GET.get("redirect")
	logout(request)
	return redirect(redirect_to)



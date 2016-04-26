from django.http import HttpResponse
from django.shortcuts import render

def index(request):
	context = {
		"user" : request.user,
		"n" : range(15), # USED FOR TESTING
	}
	return render(request, 'main/index.html', context)
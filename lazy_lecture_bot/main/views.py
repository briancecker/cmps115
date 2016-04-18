from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

def index(request):
	template = loader.get_template('lazy_lecture_bot/index.html')
	context = {}
	return HttpResponse(template.render(context, request))

def main(request):
	return render(request, "main.html", {})
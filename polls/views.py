from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader

from .models import *


def index(request):
	latest_question_list = Question.objects.all()[:5]
	#output = ', '.join([q.question_text for q in latest_question_list])

	template = loader.get_template('polls/index.html')
	context = {
		'latest_question_list': latest_question_list
	}

	return render(request, 'polls/index.html', context)

def crew_index(request):
	
	flights = FlightLeg.objects.raw('''select * from polls_flightleg 
									natural join polls_crew_participates 
									where crew_id = 1 order by time ''')

	context = {
		'upcoming_flights_list': flights
	}

	return render(request, 'polls/crew_index.html', context)	


def detail(request, question_id):
	return HttpResponse("Youre looking for question %s." % question_id)

def results(request, question_id):
	response = "Youre looking for results of question %s"
	return HttpResponse(response % question_id)

def vote(request, question_id):
	return HttpResponse("Youre voting for question %s" % question_id)

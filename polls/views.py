from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader

from .models import Question


def index(request):
	latest_question_list = Question.objects.all()[:5]
	#output = ', '.join([q.question_text for q in latest_question_list])

	template = loader.get_template('polls/index.html')
	context = {
		'latest_question_list': latest_question_list
	}

	return render(request, 'polls/index.html', context)

def detail(request, question_id):
	return HttpResponse("Youre looking for question %s." % question_id)

def results(request, question_id):
	response = "Youre looking for results of question %s"
	return HttpResponse(response % question_id)

def vote(request, question_id):
	return HttpResponse("Youre voting for question %s" % question_id)
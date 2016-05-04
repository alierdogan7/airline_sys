from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader

from polls.models import FlightLeg, Customer, Reservation


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


def cust_log(request):
	login_error = False
	if request.POST:
		
		uname = request.POST['username']
		pword = request.POST['password']
		users = Customer.objects.raw('select * from polls_customer where fullname = %s and password = %s', [uname, pword])

		u_count = 0
		for u in users:
			u_count = u_count + 1

		if (u_count == 1):
			return cust_index(request, users[0].cust_id)
		else:
			login_error = True
		
	return render(request, 'polls/cust_log.html', {'login_error':login_error}) 
		
def cust_index(request, cust_id):
	my_reserv = Reservation.objects.raw('select * from polls_reservation where cust_id = %s', [cust_id])		

	context = {
		'my_reserv_list': my_reserv
	}
	return render(request, 'polls/cust_index.html', context)

def detail(request, question_id):
	return HttpResponse("Youre looking for question %s." % question_id)

def results(request, question_id):
	response = "Youre looking for results of question %s"
	return HttpResponse(response % question_id)

def vote(request, question_id):
	return HttpResponse("Youre voting for question %s" % question_id)

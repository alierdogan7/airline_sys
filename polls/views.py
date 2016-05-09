from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import *
from polls.models import *
from django.db import connection

def index(request):
	latest_question_list = Question.objects.all()[:5]
	#output = ', '.join([q.question_text for q in latest_question_list])

	template = loader.get_template('polls/index.html')
	context = {
		'latest_question_list': latest_question_list
	}

	return render(request, 'polls/index.html', context)


"""
mail = mname.replace(" ", "_").lower() + "@gmail.com"
			hashed_pass = make_password("123")
			u = User.objects.get(email__exact=inserted.email)
		u.is_superuser = True
		u.is_staff = True
		u.save()
"""
def create_account(request):
	msg = ""
	cities = City.objects.all()
	if request.POST:
		
		mail = request.POST['email']
		pword = request.POST['pword']
		fname = request.POST['fname']
		phone = request.POST['phone']
		city = request.POST['city']

		city_obj = City.objects.get(city_name__exact=city)
		
		hashed_pass = make_password(pword)

		cust_new = Customer.objects.create(
			fullname=fname,
			password=hashed_pass,
			email=mail,
			phone=phone,
			lives_in=city_obj
		)

		user = User(username=mail, 
					email=mail,
					password=hashed_pass)
		user.save()

		msg = "Account added successfully!"

	return render(request, 'polls/create_account.html', {'city_list': cities, 'msg': msg, }) 

def crew_log(request):
	login_error = False
	if request.POST:
		
		uname = request.POST['username']
		pword = request.POST['password']
		hashed_pass = make_password(pword)
		users = Staff.objects.raw('select * from polls_staff where email = %s ', 
									[uname])

		user = authenticate(username=uname, password=pword)
		if user is not None:
			return crew_index(request, users[0].staff_id)
		else:
			login_error = True
		
	return render(request, 'polls/crew_log.html', {'login_error':login_error}) 
	
def crew_index(request, staff_id):
	flights = FlightLeg.objects.raw(''' select * from polls_flightleg where id 
										in (select flightleg_id from polls_crew_participates 
											where crew_id =  %s ) order by time ''',
											[str(staff_id)])

	context = {
		'upcoming_flights_list': flights
	}

	return render(request, 'polls/crew_index.html', context)


def cust_log(request):
	login_error = False
	if request.POST:
		
		email = request.POST['email']
		pword = request.POST['password']
		hashed_pass = make_password(pword)
		customer = Customer.objects.raw('''select * from polls_customer where 
									email = %s''', 
									[email])
		user = authenticate(username=email, password=pword)

		customer = customer[0]
		if user is not None and customer is not None:
			return cust_index(request, customer.cust_id)
		else:
			login_error = True
		
	return render(request, 'polls/cust_log.html', {'login_error':login_error}) 
		

def cust_index(request, cust_id):
	my_reserv = Reservation.objects.raw('select * from polls_reservation where cust_id = %s', [cust_id])		

	context = {
		'my_reserv_list': my_reserv
	}
	return render(request, 'polls/cust_index.html', context)


def reports(request):
	cursor = connection.cursor()
	
	# RETRIEVE SALESMEN
	cursor.execute("""CREATE TEMPORARY TABLE IF NOT EXISTS active_salesmen
				AS (SELECT S.fullname, COUNT(*) AS sales
					FROM polls_reservation R, polls_staff S
					WHERE S.staff_id = R.sold_by_id
					AND R.reservation_time >= DATE_FORMAT(CURDATE(),  '%Y-%m-01')
					GROUP BY sold_by_id
					ORDER BY sales DESC)""")
	cursor.execute("SELECT fullname, sales FROM active_salesmen")		
	salesmen = [ {'fullname': row[0], 'sales': row[1]} for row in cursor.fetchall() ]
	
	cursor.execute("""CREATE TEMPORARY TABLE IF NOT EXISTS total_distances AS 
					(SELECT cust_id, SUM(travel_distance) AS total
					        FROM polls_reservation R, polls_flightleg F
					        WHERE R.flight_leg_id = F.id
					        AND F.time >= DATE_FORMAT(CURDATE(), '%Y-%m-01') - INTERVAL 2 MONTH
					        GROUP BY cust_id) """)
	cursor.execute("""SELECT fullname, total 
						FROM total_distances JOIN polls_customer USING (cust_id) 
						WHERE total > 1000 ORDER BY total DESC """)
	customers = [ {'fullname': row[0], 'total_travel': row[1]} for row in cursor.fetchall() ]

	context = {'salesmen' : salesmen, 'customers': customers}
	return render(request, 'admin/reports.html', context)

def detail(request, question_id):
	return HttpResponse("Youre looking for question %s." % question_id)

def results(request, question_id):
	response = "Youre looking for results of question %s"
	return HttpResponse(response % question_id)

def vote(request, question_id):
	return HttpResponse("Youre voting for question %s" % question_id)

from django.shortcuts import render, redirect

# Create your views here.
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, logout
from django.contrib.auth.hashers import *
from polls.models import *
from polls.utils import *
from datetime import datetime
from django.db import connection
import random

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
	cursor = connection.cursor()
	cursor.execute(''' SELECT * FROM upcoming_flights WHERE crew_id = %s ''',
											[str(staff_id)])
	flights = []
	for row in cursor.fetchall():
		flights.append({
				'flight_leg_code': row[0],
				'time': row[1],
				'departs': row[2],
				'estimated_arr_time': row[3],
				'arrives': row[4],
				'travel_distance': row[5],
				'plane': row[7],
				'is_cancelled': True if row[6] else False
			})
	
	context = {
		'upcoming_flights_list': flights
	}

	return render(request, 'polls/crew_index.html', context)


def cust_log(request):
	login_error = False
	cust_id = request.session.get('cust_id', '')
	if (not cust_id) and request.user.is_authenticated():
		return redirect('cust_index')

	if request.POST:
		
		email = request.POST['email']
		pword = request.POST['password']
		hashed_pass = make_password(pword)
		customer = Customer.objects.raw('''select * from polls_customer where 
									email = %s''', 
									[email])
		user = authenticate(username=email, password=pword)
		
		if user is not None and customer is not None:
			customer = customer[0]
			request.session['cust_id'] = customer.cust_id
			#return cust_index(request, customer.cust_id)
			return redirect('cust_index')
		else:
			login_error = True
		
	return render(request, 'polls/cust_log.html', {'login_error':login_error}) 
		

def cust_logout(request):
    logout(request)	
    return redirect('cust_log')	
    
def cust_index(request):
	cust_id = request.session.get('cust_id', '')
	my_reserv = Reservation.objects.raw('select * from polls_reservation where cust_id = %s', [cust_id])		

	msg = ""
	
	if(request.GET.get('delete')):
		res_code = request.GET.get('reserv_code')
		Reservation.objects.get(reservation_code = res_code).delete()
		msg = "Reservation with code " + res_code + " deleted successfully"
	
	if(request.GET.get('buy')):
		res_code = request.GET.get('reserv_code')
		
		# class Ticket(models.Model):
		# ticket_no = models.AutoField(primary_key=True)
		# original_price = models.IntegerField(null=False)
		# discounted_price = models.IntegerField(null=True)
		# promotion = models.ForeignKey(Promotion, null=True)
		# reservation_code = models.ForeignKey(Reservation, db_column='reservation_code', null=False)

		#fl = FlightLeg.objects.get(reservation_code = res_code)
		res = Reservation.objects.get(pk = res_code)
		fl = res.flight_leg
		Ticket.objects.create(original_price = fl.price_for_business, reservation_code = res)
		
		msg = "Reservation with code " + res_code + " ticket bought with price : " + str(fl.price_for_business)

	context = {
		'my_reserv_list': my_reserv,
		'msg': msg,
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

	context = {
	'salesmen': salesmen,
	'customers': customers
	}

	return render(request, 'admin/reports.html', context)

def new_reserv(request):
	
	#available_flights = FlightLeg.objects.raw('select distinct * from polls_flightleg order by time')
	airports = Airport.objects.raw('select * from polls_airport order by airport_code')
	listing = True
	available_flights = []

	if(request.GET.get('select_dep_port') and request.GET.get('select_arr_port')):
		ind_dep = int(request.GET.get('select_dep_port'))
		dep_port = airports[ind_dep].airport_name
		
		ind_arr = int(request.GET.get('select_arr_port'))
		arr_port = airports[ind_arr].airport_name

		available_flights = find_flight(dep_port, arr_port)
		val = ""
		print available_flights
		for fli in available_flights:
			for f in fli:
				val += str(f) + "-"
			val += "\n"

		#return HttpResponse(val)

		listing = False
		
	context = {
		'available_flights':available_flights,
		'airports': airports,
		'listing':listing,
	}
	return render(request, 'polls/new_reserv.html', context)

def fl_view(request, fl_id):
	cursor = connection.cursor()
	cursor.execute('''select S.seat_number, S.seat_letter from polls_reservation R, polls_seat S, polls_flightleg L where L.id = %s and R.seat_id = S.id and R.flight_leg_id =  L.id ''', [fl_id])
	full_seats = [ {'seat_number': int(row[0]), 'seat_letter': str(row[1]) } for row in cursor.fetchall() ]

	#return HttpResponse(full_seats[0]['seat_letter'])
	my_fl = FlightLeg.objects.raw('select * from polls_flightleg where id = %s', [fl_id])
	fl = my_fl[0]
	plane_id = fl.plane_id.plane_id
	plane = Plane.objects.raw('select * from polls_plane where plane_id = %s', [plane_id])[0]
	
	total_count = plane.no_of_seats
	full_count = len(full_seats)

	empty_seats = []
	for number in xrange(1, plane.no_of_seats / plane.seats_per_row + 1):
		for letter in xrange(ord('A'), ord('A') + plane.seats_per_row):
			if not in_full_seats(full_seats, number, chr(letter) ):
				empty_seats.append({'number':number, 'letter': chr(letter) })

	context = {
		'empty_seats': empty_seats,
		'full_count': full_count,
		'total_count': total_count,
	}

	if request.GET.get('reserve'):
		ind = int(request.GET.get('select_seat', 0))
		my_seat = Seat.objects.get(seat_number = empty_seats[ind]['number'], seat_letter = empty_seats[ind]['letter'], plane_id = plane_id)
		
		extra_lug = False
		alphabet = [ chr(char) for char in xrange(ord('A'), ord('Z') + 1) ] 
		
		cust = Customer.objects.get(pk=request.session.get('cust_id', ''))
		my_fl = FlightLeg.objects.get(pk=fl_id)

		args = {
			"reservation_code": "".join(random.sample(alphabet, 6)),
			"cust_id": cust,
			"flight_leg": my_fl,
			"seat": my_seat,
			"sold_by": None,
			"extra_luggage": extra_lug,
		}
		res_code = "".join(random.sample(alphabet, 6))
		Reservation.objects.create(reservation_code=res_code, cust_id=cust, flight_leg=my_fl, seat = my_seat,sold_by=None, extra_luggage = extra_lug)
		
	return render(request, 'polls/flight_view.html', context)

def in_full_seats(full_seats, n, l):
	for seat in full_seats:
		if n == seat['seat_number'] and l == seat['seat_letter']:
			return True
	return False


def cust_tickets(request):
	cust_id = request.session.get('cust_id', '')
	my_tickets = Ticket.objects.filter(reservation_code__cust_id = cust_id)

	Ticket.objects.filter
	context = {
		'my_tickets': my_tickets
	}
	return render(request, 'polls/cust_tickets.html', context)

def cust_profile(request):
	#my_reserv = Reservation.objects.raw('select * from polls_reservation where cust_id = %s', [cust_id])		

	context = {
		'my_reserv_list': ''
	}
	return render(request, 'polls/cust_profile.html', context)

def detail(request, question_id):
	return HttpResponse("Youre looking for question %s." % question_id)

def results(request, question_id):
	response = "Youre looking for results of question %s"
	return HttpResponse(response % question_id)

def vote(request, question_id):
	return HttpResponse("Youre voting for question %s" % question_id)

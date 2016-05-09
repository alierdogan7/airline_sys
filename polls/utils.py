from django.test import TestCase
from django.utils import timezone
from polls.models import *
from django.contrib.auth.models import User, Group
from django.contrib.auth.hashers import *
import random
import datetime
from django.db import connection

# Create your tests here.

def init_cities():
	City.objects.all().delete()
	cities = [	'Ankara', 'Istanbul', 
					'Izmir', 'Gaziantep',
					'Eskisehir'
				]

	for cityname in cities:
		City.objects.create(city_name=cityname)

def init_airports():
	Airport.objects.all().delete()
	for city in City.objects.all():
		airp_code = ((city.city_name)[:3]).upper()
		supports = True if city.city_name in ['Ankara', 'Istanbul'] else False
		city.airport_set.create(
						airport_code=airp_code,
						airport_name=city.city_name + ' Havalimani',
						max_airplanes=100,
						city_name=city,
						supports_flight_legs=supports
					)

def init_customers():
	Customer.objects.all().delete()
	names = [ 'Clarke Martinez',
				'Erasmus York',
				'Tucker Cook',
				'Hunter Casey',
				'Phillip Pitts',
				'Hector Curtis',
				'Phillip Joseph',
				'Dustin Morris',
				'Benedict Pennington',
				'Warren Murray',
				'Tucker Blanchard',
				'Finn Glover',
				'Timothy Morrison',
				'Forrest Riddle',
				'Darius Beach',
				'Nolan Leonard',
				'Joel Yates',
				'Colby Durham',
				'Elvis Wyatt',
				'Wyatt Hayes' ]


	cities = City.objects.all()
	for cname in names:
		mail = cname.replace(" ", "_").lower() + "@gmail.com"
		hashed_pass = make_password("123")

		Customer.objects.create(
			fullname=cname,
			password=hashed_pass,
			email=mail,
			phone='03403043',
			lives_in=random.choice(cities)
			)

		user = User(username=mail, 
					email=mail,
					password=hashed_pass)
		user.save()


# CLOSURE FOR PRODUCING INIT FUNCTIONS OF DIFFERENT STAFF TYPES
def make_init_staff(staff_type, create_func):
	def init_x(names):
		# clear the staff tuples, 
		#and managers will be cleaned automatically
		for s in staff_type.objects.all():
			s.staff_id.delete()

		airports = Airport.objects.all()
		inserted_staffs = []
		for mname in names:
			mail = mname.replace(" ", "_").lower() + "@gmail.com"
			hashed_pass = make_password("123")

			inserted_staffs.append(
				Staff.objects.create(
				fullname=mname,
				password=hashed_pass,
				email=mail,
				phone='03403011',
				salary=random.randrange(1000, 5000, 200),
				works_in=random.choice(airports)
			))

			user = User(username=mail, 
					email=mail,
					password=hashed_pass)
			user.save()

		for inserted in inserted_staffs:
			create_func(inserted)

	return init_x

def init_all_staff():
	def c_salesman(inserted):
		Salesman.objects.create(staff_id=inserted)
		# set group permissions of salesman
		u = User.objects.get(email__exact=inserted.email)
		u.groups.add(Group.objects.get(name__exact="Salesman"))
		u.is_staff = True
		u.save()

	def c_manager(inserted):
		Manager.objects.create (
				staff_id=inserted,
				degree='full'
			)
		# set manager permissions
		u = User.objects.get(email__exact=inserted.email)
		u.is_superuser = True
		u.is_staff = True
		u.save()

	def c_pilot(inserted):
		Crew.objects.create(staff_id=inserted)
		Pilot.objects.create(staff_id=inserted, license_type='national')

	def c_hostess(inserted):
		Crew.objects.create(staff_id=inserted)
		Hostess.objects.create(staff_id=inserted, mother_language='English')


	manager_names = [
		'Howard Robinson',
		'Lance Nash',
		'Ali Burak',
		'Yusuf Said',
		'Abdullah Alperen'
	]

	salesmen_names = [
		'Vernon Owens',
		'Abel Manning',
		'Stewart Hendricks',
	]

	pilot_names = [
		'Vaughan Emerson',
		'Ian Baker',
		'Caleb Barlow',
		'Beau Dennis',
		'Thanh Zabriskie',
	]

	hostess_names = [	
		'Dane Hill',
		'Denton Alexander',
		'Kyle English',
		'Zachery Briggs',
		'Elton Nicholson',
		'Annabel Romanowski', 
		'Jeannie Nunemaker', 
		'Kimberlee Ravelo', 
		'Rich Liechty', 
		'Peg Mcnamara', 
	]


	init_managers = make_init_staff(Manager, c_manager)
	init_salesmen = make_init_staff(Salesman, c_salesman)
	init_pilots = make_init_staff(Pilot, c_pilot)
	init_hostess = make_init_staff(Hostess, c_hostess)

	init_managers(manager_names)
	init_salesmen(salesmen_names)
	init_pilots(pilot_names)
	init_hostess(hostess_names)


def init_planes():
	Plane.objects.all().delete()

	planes = [
		("Boeing-707", "2000", 180),
		("Airbus A380", "1996", 240),
		("Boeing-550", "1992", 120),
		("Minicraft", "1991", 60),
	]

	for plane in planes:
		p = Plane.objects.create(model=plane[0],
							production_year=plane[1],
							no_of_seats=plane[2])
		p.gen_seats()

def init_flight_legs():
	FlightLeg.objects.all().delete()

	airports = Airport.objects.all()
	planes = Plane.objects.all()
	hostesses = Hostess.objects.all()
	pilots = Pilot.objects.all()

	for i in xrange(60):
		rand_plane = random.choice(planes)
		price_for_economy = random.randrange(100,400,30)
		time = timezone.now() + datetime.timedelta(days=random.randint(1,60), hours=random.randint(1,24))
		selected_airports = random.sample(airports, 2)
		
		args = {
			"flight_leg_code": "TK-7" + str(random.randint(100,300)),
		    "time":  time,
		    "estimated_arr_time": time + datetime.timedelta(minutes=random.randint(60, 250)),
		    "plane_id": rand_plane,
		    "no_of_available_seats": rand_plane.no_of_seats,
		    "travel_distance": random.randint(800,2000),
		    "price_for_economy": price_for_economy,
		    "price_for_business": price_for_economy + 200,
			"arrives": selected_airports[0],    
			"departs": selected_airports[1]
		}

		flightleg = FlightLeg.objects.create(**args)
		for crew in random.sample(hostesses, 2) + random.sample(pilots, 2):
			flightleg.crew_set.add(Crew.objects.get(pk=crew.staff_id))



def init_reservations():
	Reservation.objects.all().delete()

	alphabet = [ chr(char) for char in xrange(ord('A'), ord('Z') + 1) ] 
	customers = Customer.objects.all()
	flight_legs = FlightLeg.objects.all()
	salesmen = Salesman.objects.all()

	new_reservations = []
	for i in xrange(20 * len(flight_legs)):
		flight_leg = random.choice(flight_legs)
		args = {
			"reservation_code": "".join(random.sample(alphabet, 6)),
			"cust_id": random.choice(customers),
			"flight_leg": flight_leg,
			"seat": random.choice(flight_leg.plane_id.seat_set.all()),
			"sold_by": random.choice(salesmen),
			"extra_luggage": random.choice([True, False])
		}
		new_reservations.append( Reservation(**args) )


	Reservation.objects.bulk_create(new_reservations)	

def find_flight(source, destination):
	all_flights = [ fl for fl in FlightLeg.objects.order_by('time') ]
	source = Airport.objects.get(airport_name__exact=source)
	destination = Airport.objects.get(airport_name__exact=destination)
	visited_list = []
	
	possible_flights = []
	flight_list = search_flight(source, destination, all_flights, visited_list)
	while flight_list:
		print "Possible flight:"
		for f in flight_list:
			print "%s %s --> %s " % (f, f.departs, f.arrives )
		possible_flights.append(flight_list)
		# filter the flights
		all_flights = [ flight for flight in all_flights if flight not in flight_list ] 
		flight_list = search_flight(source, destination, all_flights, visited_list)

	return possible_flights

def search_flight(source, destination, flights, visited_list):
	if flights is not None and len(flights) > 0:
		flight = flights[0]
		if source == flight.departs and (flight.arrives.city_name not in visited_list):
			visited_list.append(flight.departs.city_name) #source city is visited
			if flight.arrives == destination:
				return [flight]
			elif flight.arrives.supports_flight_legs:
				return [flight] + search_flight(flight.arrives, destination, flights[1:], visited_list)
			else:
				return search_flight(source, destination, flights[1:], visited_list)
		else:
			return search_flight(source, destination, flights[1:], visited_list)
	else: #base case
		return []

def trunc_users():
	User.objects.all().delete()	

def set_triggers():
	cursor = connection.cursor()

	cursor.execute("""CREATE TRIGGER after_reservation
						AFTER INSERT ON polls_reservation
						FOR EACH ROW
						BEGIN
							UPDATE polls_salesman
							SET no_of_tickets_sold = no_of_tickets_sold + 1
							WHERE staff_id = NEW.sold_by_id;
						UPDATE polls_flightleg
							SET no_of_available_seats = no_of_available_seats - 1
							WHERE id = NEW.flight_leg_id;
						END;""")

def init():
	print "truncating users table..."
	trunc_users()

	print "initializing cities..."
	init_cities()

	print "initializing airports..."
	init_airports()

	print "initializing customers..."
	init_customers()
	
	print "initializing all staff..."
	init_all_staff()
	
	print "initializing planes..."
	init_planes()
	
	print "initializing flight legs..."
	init_flight_legs()

	print "initializing reservations..."
	init_reservations()

	print "setting triggers..."
	set_triggers()
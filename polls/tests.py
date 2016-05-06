from django.test import TestCase
from django.utils import timezone
from polls.models import *
from django.contrib.auth.models import User, Group
from django.contrib.auth.hashers import *
import random
import datetime

# Create your tests here.

def init_cities():
	City.objects.all().delete()
	cities = [	'Ankara', 'Istanbul', 
					'Izmir', 'Gaziantep',
					'Eskisehir', 'Adana',
					'Bursa', 'Mersin'
				]

	for cityname in cities:
		City.objects.create(city_name=cityname)

def init_airports():
	Airport.objects.all().delete()
	for city in City.objects.all():
		airp_code = ((city.city_name)[:3]).upper()
		city.airport_set.create(
						airport_code=airp_code,
						airport_name=city.city_name + ' Havalimani',
						max_airplanes=100,
						city_name=city
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
	]

	hostess_names = [	
		'Dane Hill',
		'Denton Alexander',
		'Kyle English',
		'Zachery Briggs',
		'Elton Nicholson'
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
	airports = Airport.objects.all()
	planes = Plane.objects.all()

	for i in xrange(10):
		rand_plane = random.choice(planes)
		price_for_economy = random.randrange(100,400,30)
		time = timezone.now() + datetime.timedelta(days=random.randint(1,60))
		selected_airports = random.sample(airports, 2)
		
		args = {
			"flight_leg_code": "TK-7" + str(random.randint(100,300)),
		    "time":  time,
		    "estimated_arr_time": time + datetime.timedelta(minutes=random.randint(60, 250)),
		    "plane_id": rand_plane,
		    "no_of_available_seats": rand_plane.no_of_seats,
		    "travel_distance": random.randint(800,2000, 100),
		    "price_for_economy": price_for_economy,
		    "price_for_business": price_for_economy + 200,
			"arrives": selected_airports[0],    
			"departs": selected_airports[1]
		}

		FlightLeg.objects.create(**args)

def init_reservations():
	alphabet = [ chr(char) for char in xrange(ord('A'), ord('Z') + 1) ] 
	customers = Customer.objects.all()
	flight_legs = FlightLeg.objects.all()
	salesmen = Salesman.objects.all()

	for i in xrange(len(customers)):
		flight_leg = random.choice(flight_legs)
		args = {
			"reservation_code": "".join(random.sample(alphabet, 6)),
			"cust_id": random.choice(customers),
			"flight_leg": flight_leg,
			"seat": random.choice(flight_leg.plane_id.seat_set.all()),
			"sold_by": random.choice(salesmen),
			"extra_luggage": random.choice([True, False])
		}

		Reservation.objects.create(**args)

def trunc_users():
	User.objects.all().delete()

def init():
	print "truncating users table"
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
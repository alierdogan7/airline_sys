from django.test import TestCase
from polls.models import *
import random

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
		Customer.objects.create(
			fullname=cname,
			password='123',
			email='abc@gmail.com',
			phone='03403043',
			lives_in=random.choice(cities)
			)

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
			inserted_staffs.append(
				Staff.objects.create(
				fullname=mname,
				password='123',
				email='staff@gmail.com',
				phone='03403011',
				salary=random.randrange(1000, 5000, 200),
				works_in=random.choice(airports)
			))

		for inserted in inserted_staffs:
			create_func(inserted)

	return init_x

def init_all_staff():
	def c_salesman(inserted):
		Salesman.objects.create(staff_id=inserted)

	def c_manager(inserted):
		Manager.objects.create (
				staff_id=inserted,
				degree='full'
			)

	def c_pilot(inserted):
		Crew.objects.create(staff_id=inserted)
		Pilot.objects.create(staff_id=inserted, license_type='national')

	def c_hostess(inserted):
		Crew.objects.create(staff_id=inserted)
		Hostess.objects.create(staff_id=inserted, mother_language='English')


	manager_names = [
		'Howard Robinson',
		'Lance Nash'
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




def init():
	init_cities()
	init_airports()
	init_customers()
	init_all_staff()
	

init()
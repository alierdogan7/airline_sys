from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Question(models.Model):
	question_text = models.CharField(max_length=200)
	pub_date = models.DateTimeField('date published')

	def __str__(self):
		return self.question_text

class Choice(models.Model):
	question = models.ForeignKey(Question, on_delete=models.CASCADE)
	choice_text = models.CharField(max_length=200)
	votes = models.IntegerField(default=0)

	def __str__(self):
		return self.choice_text

###############################


class City(models.Model):
	city_name = models.CharField(max_length=50, primary_key=True)
	no_of_airports = models.PositiveSmallIntegerField(default=0)

	def __str__(self):
		return self.city_name

class Airport(models.Model):
	airport_code = models.CharField(max_length=20, primary_key=True)
	airport_name = models.CharField(max_length=100, null=False)
	supports_flight_legs = models.BooleanField(default=False)
	max_airplanes = models.PositiveSmallIntegerField(null=False)
	city_name = models.ForeignKey(City, on_delete=models.CASCADE, db_column='city_name')

	def __str__(self):
		return "%s (%s)" % (self.airport_name, self.airport_code)

class Customer(models.Model):
	cust_id = models.AutoField(primary_key=True)
	password = models.CharField(max_length=128, null=False)
	fullname = models.CharField(max_length=100, null=False)
	email = models.EmailField(null=False)
	phone = models.CharField(max_length=20, null=False)
	last_login = models.DateTimeField('last login', null=True)
	no_of_flights = models.PositiveSmallIntegerField(default=0)
	lives_in = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, db_column='lives_in')
	flights = models.ManyToManyField('Flight')
	
	class Meta:
		unique_together = ("fullname", "password")

	def __str__(self):
		return self.fullname

class Staff(models.Model):
	staff_id = models.AutoField(primary_key=True)
	password = models.CharField(max_length=128, null=False)
	fullname = models.CharField(max_length=100, null=False)
	email = models.EmailField(null=False)
	phone = models.CharField(max_length=20, null=False)
	last_login = models.DateTimeField('last login', null=True)
	salary = models.IntegerField(default=0)
	manager_id = models.ForeignKey('Manager', on_delete=models.SET_NULL, blank=True ,null=True, db_column='manager_id')
	works_in = models.ForeignKey(Airport, on_delete=models.SET_NULL, null=True, db_column='works_in')

	def __str__(self):
		return self.fullname

class Manager(models.Model):
 	staff_id = models.OneToOneField(
 				Staff,
 				on_delete=models.CASCADE,
 				primary_key=True,
 				db_column='staff_id')

 	DEGREE = (
 		("full", "full authorization"),
 		("partial", "partial authorization"),
 	)
 	degree = models.CharField(max_length=100, null=False, choices=DEGREE)

 	def __str__(self):
 		return self.staff_id.fullname

class Salesman(models.Model):
 	staff_id = models.OneToOneField(
 				Staff,
 				on_delete=models.CASCADE,
 				primary_key=True,
 				db_column='staff_id')
 	
 	no_of_sold_tickets = models.PositiveSmallIntegerField(default=0)

 	def __str__(self):
 		return self.staff_id.fullname

class Plane(models.Model):
	plane_id = models.AutoField(primary_key=True)
	model = models.CharField(max_length=130, null=False)
	production_year = models.CharField(max_length=4, null=False)
	no_of_seats = models.PositiveSmallIntegerField(null=False)
	seats_per_row = models.PositiveSmallIntegerField(null=False, default=6)

	def __str__(self):
		return "%s (ID: %s)" % (self.model, self.plane_id)

	def gen_seats(self):
		if self.no_of_seats % self.seats_per_row != 0:
			print "invalid options."
			return	
		else:
			#generate seats
			all_seats = []
			for number in xrange(1, self.no_of_seats / self.seats_per_row + 1):
				for letter in xrange(ord('A'), ord('A') + self.seats_per_row):
					klass = "business" if number <= 3 else "economy"
					all_seats.append( Seat(plane_id=self, seat_number=number, 
											seat_letter=chr(letter), seat_class=klass) )
					#self.seat_set.create(seat_number=number, seat_letter=chr(letter))			
			self.seat_set.bulk_create(all_seats) #for quickly inserting all the tuples


class Seat(models.Model):
	seat_number = models.PositiveSmallIntegerField(null=False)
	seat_letter = models.CharField(max_length=1, null=False)
	plane_id = models.ForeignKey(Plane, on_delete=models.CASCADE, db_column='plane_id', null=False)

	SEAT_CLASSES = (
			('business', 'BusinessClass'),
			('economy', 'EconomyClass'),
	)
	seat_class = models.CharField(max_length=20, null=False, choices=SEAT_CLASSES)

	class Meta:
		unique_together = ("seat_letter", "seat_number", "plane_id")

	def __str__(self):
		return "%d%s" % (self.seat_number, self.seat_letter)
		

class Crew(models.Model):
 	staff_id = models.OneToOneField(
 				Staff,
 				on_delete=models.CASCADE,
 				primary_key=True,
 				db_column='staff_id')
 	
	num_of_flights = models.PositiveSmallIntegerField(default=0)
	since = models.DateField(auto_now_add=True)
	participates = models.ManyToManyField('FlightLeg')

 	def __str__(self):
 		return self.staff_id.fullname

class Pilot(models.Model):
 	staff_id = models.OneToOneField(
 				Staff,
 				on_delete=models.CASCADE,
 				primary_key=True,
 				db_column='staff_id')
 	
	LICENSE_TYPES = (
			("national", "only in a country"),
			("international", "international flights"),
	)
	license_type = models.CharField(max_length=101, null=False, choices=LICENSE_TYPES)

 	def __str__(self):
 		return "Pilot " + self.staff_id.fullname

class Hostess(models.Model):
 	staff_id = models.OneToOneField(
 				Staff,
 				on_delete=models.CASCADE,
 				primary_key=True,
 				db_column='staff_id')
 	
	mother_language = models.CharField(max_length=30)
	first_aid_ability = models.BooleanField(default=False)

 	def __str__(self):
		return "Hostess " + self.staff_id.fullname

class FlightLeg(models.Model):
	flight_leg_code = models.CharField(max_length=7, null=False)
	time = models.DateTimeField(null=False)
	estimated_arr_time = models.DateTimeField(null=False)
	arrives = models.ForeignKey(Airport, related_name='landing_flights', on_delete=models.CASCADE, db_column='arrives', null=False)
	departs = models.ForeignKey(Airport, related_name='departing_flights', on_delete=models.CASCADE, db_column='departs', null=False)
	plane_id = models.ForeignKey(Plane, on_delete=models.CASCADE, db_column='plane_id', null=False)
	no_of_available_seats = models.PositiveSmallIntegerField(null=False)
	is_cancelled = models.BooleanField(default=False)
	travel_distance = models.IntegerField(null=False)
	price_for_economy = models.IntegerField(null=False)
	price_for_business = models.IntegerField(null=False)

	class Meta:
		unique_together = ("flight_leg_code", "time")

	def __str__(self):
		return "%s (Departs: %s)" % (self.flight_leg_code, self.time)
		

class Reservation(models.Model):
	reservation_code = models.CharField(max_length=6, primary_key=True)
	cust_id = models.ForeignKey(Customer, db_column='cust_id', null=False)
	flight_leg = models.ForeignKey(FlightLeg, null=False)
	seat = models.ForeignKey(Seat, null=False)
	sold_by = models.ForeignKey(Salesman, null=True, blank=True)
	extra_luggage = models.BooleanField(default=False)
	reservation_time = models.DateTimeField(auto_now_add=True)
	
	def __str__(self):
		return "%s" % (self.reservation_code)

class Promotion(models.Model):
	promotion_id = models.AutoField(primary_key=True)
	discount_percent = models.PositiveSmallIntegerField(null=False)
	last_valid_date = models.DateTimeField(null=False)
	given_cust = models.ForeignKey(Customer, null=False)

class Ticket(models.Model):
	ticket_no = models.AutoField(primary_key=True)
	original_price = models.IntegerField(null=False)
	discounted_price = models.IntegerField(null=True)
	promotion = models.ForeignKey(Promotion, null=True)
	reservation_code = models.ForeignKey(Reservation, db_column='reservation_code', null=False)

class Flight(models.Model):
	flight_id = models.AutoField(primary_key=True)
	no_of_legs = models.PositiveSmallIntegerField(default=0)
	total_time_in_mins = models.PositiveSmallIntegerField(default=0)
	total_distance_in_kms = models.PositiveSmallIntegerField(default=0)
	legs = models.ManyToManyField('FlightLeg')

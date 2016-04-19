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
	no_of_airports = models.IntegerField(default=0)

	def __str__(self):
		return self.city_name

class Airport(models.Model):
	airport_code = models.CharField(max_length=20, primary_key=True)
	airport_name = models.CharField(max_length=100, null=False)
	supports_flight_legs = models.BooleanField(default=False)
	max_airplanes = models.IntegerField(null=False)
	city_name = models.ForeignKey(City, on_delete=models.CASCADE)

	def __str__(self):
		return "%s (%s)" % (self.airport_name, self.airport_code)

class Customer(models.Model):
	cust_id = models.AutoField(primary_key=True)
	password = models.CharField(max_length=20, null=False)
	fullname = models.CharField(max_length=100, null=False)
	email = models.EmailField(null=False)
	phone = models.CharField(max_length=20, null=False)
	last_login = models.DateTimeField('last login', null=True)
	no_of_flights = models.IntegerField(default=0)
	lives_in = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)

	def __str__(self):
		return self.fullname

class Staff(models.Model):
	staff_id = models.AutoField(primary_key=True)
	password = models.CharField(max_length=20, null=False)
	fullname = models.CharField(max_length=100, null=False)
	email = models.EmailField(null=False)
	phone = models.CharField(max_length=20, null=False)
	last_login = models.DateTimeField('last login', null=True)
	salary = models.IntegerField(default=0)
	manager_id = models.ForeignKey('self', on_delete=models.SET_NULL, null=True)
	works_in = models.ForeignKey(Airport, on_delete=models.CASCADE)

	def __str__(self):
		return self.fullname

# class Manager(models.Model):
# 	staff_id = models.ForeignKey(Staff, primary_key=True)
# 	degree = models.CharField(max_length=100)

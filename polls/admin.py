from django.contrib import admin

# Register your models here.
from .models import *

def admin_site_customization():
	site = admin.sites.AdminSite
	site.site_header = 'Airline Company Management System'

admin_site_customization()

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):

	list_display = ('reservation_code', 'cust_id', 'flight_leg', 'seat', 'reservation_time', 'sold_by', 'extra_luggage')
	search_fields = ['reservation_code', 'cust_id__fullname']

@admin.register(FlightLeg)
class FlightLegAdmin(admin.ModelAdmin):
	list_display = ('flight_leg_code', 'time', 'estimated_arr_time',
					'arrives', 'departs', 'plane_id', 'no_of_available_seats',
					'travel_distance', 'price_for_economy', 'price_for_business',
					'is_cancelled')

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
	list_display = ('city_name', 'no_of_airports')


@admin.register(Airport)
class AirportAdmin(admin.ModelAdmin):
	list_display = ('airport_code', 'airport_name',
						'supports_flight_legs', 'max_airplanes',
						'city_name')

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
	list_display = ('cust_id', 'fullname', 'email', 'phone', 'last_login',
					'no_of_flights', 'lives_in'
					)

@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
	list_display = ('staff_id', 'fullname', 'email', 
					'phone', 'last_login', 'salary', 
					'manager_id', 'works_in')
					

@admin.register(Manager)
class ManagerAdmin(admin.ModelAdmin):
	list_display = ('staff_id', 'degree')

@admin.register(Salesman)
class SalesmanAdmin(admin.ModelAdmin):
	list_display = ('staff_id','no_of_sold_tickets')

@admin.register(Crew)
class CrewAdmin(admin.ModelAdmin):
	list_display = ('staff_id', 'num_of_flights', 'since')

@admin.register(Pilot)
class PilotAdmin(admin.ModelAdmin):
	list_display = ('staff_id', 'license_type')

@admin.register(Hostess)
class HostessAdmin(admin.ModelAdmin):
	list_display = ('staff_id', 'mother_language', 'first_aid_ability')

@admin.register(Plane)
class PlaneAdmin(admin.ModelAdmin):
	list_display = ('plane_id', 'model', 
					'production_year', 'no_of_seats',
					'seats_per_row')

@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
	list_display = ('seat_number', 'seat_letter', 'plane_id')

@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
	list_display = ('promotion_id', 'discount_percent',
					'last_valid_date', 'given_cust')

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
	list_display = ('ticket_no', 'original_price',
					'discounted_price', 'promotion',
					'reservation_code')

@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
	list_display = ('flight_id', 'no_of_legs',
					'total_time_in_mins', 'total_distance_in_kms',
					)

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

admin.site.register(City)
admin.site.register(Airport)
admin.site.register(Customer)
admin.site.register(Staff)
admin.site.register(Manager)
admin.site.register(Salesman)
admin.site.register(Plane)
admin.site.register(Seat)
admin.site.register(Crew)
admin.site.register(Pilot)
admin.site.register(Hostess)

admin.site.register(Promotion)
admin.site.register(Ticket)
admin.site.register(Flight)
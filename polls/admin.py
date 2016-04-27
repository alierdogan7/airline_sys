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
admin.site.register(FlightLeg)


from django.contrib import admin

# Register your models here.
from .models import *

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
admin.site.register(Reservation)


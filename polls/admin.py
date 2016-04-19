from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Question)
admin.site.register(Customer)
admin.site.register(Staff)
admin.site.register(Airport)
admin.site.register(City)

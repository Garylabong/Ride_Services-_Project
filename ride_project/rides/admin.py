from django.contrib import admin
from rides.models import User, Ride, RideEvent

admin.site.register(User)

admin.site.register(Ride)
admin.site.register(RideEvent)
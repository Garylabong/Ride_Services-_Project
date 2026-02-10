from django.contrib import admin
from rides.models import User, Ride, RideEvent


# class AuthorAdmin(admin.ModelAdmin):
#     pass


admin.site.register(User)

admin.site.register(Ride)
admin.site.register(RideEvent)
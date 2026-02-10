from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('rider', 'Rider'),
        ('driver', 'Driver')
    )

    id_user = models.AutoField(primary_key=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)


class Ride(models.Model):

    STATUS_CHOICES = (
        ('en-route', 'En Route'),
        ('pickup', 'Pickup'),
        ('dropoff', 'Dropoff')
    )

    id_ride = models.AutoField(primary_key=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    id_rider = models.ForeignKey(
        User, related_name="rides_as_rider", on_delete=models.CASCADE
    )
    id_driver = models.ForeignKey(
        User, related_name="rides_as_driver", on_delete=models.CASCADE
    )

    pickup_latitude = models.FloatField()
    pickup_longitude = models.FloatField()
    dropoff_latitude = models.FloatField()
    dropoff_longitude = models.FloatField()
    pickup_time = models.DateTimeField()

    class Meta:
        indexes = [
            models.Index(fields=["id_driver"]),
            models.Index(fields=["pickup_time"]),
        ]



class RideEvent(models.Model):

    id_ride_event = models.AutoField(primary_key=True)
    id_ride = models.ForeignKey(
        Ride, related_name="ride_events", on_delete=models.CASCADE
    )

    description = models.CharField(max_length=255)
    created_at = models.DateTimeField()

    class Meta:
        indexes = [
            models.Index(fields=["id_ride", "description"]),
            models.Index(fields=["created_at"]),
        ]
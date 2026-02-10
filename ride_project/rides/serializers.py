from rest_framework import serializers
from .models import Ride, RideEvent, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id_user', 'email', 'first_name', 'last_name', 'role']


class RideEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = RideEvent
        fields = ['id_ride_event', 'description', 'created_at']


class RideSerializer(serializers.ModelSerializer):

    rrider = UserSerializer(source="id_rider", read_only=True)
    driver = UserSerializer(source="id_driver", read_only=True)
    todays_ride_events = RideEventSerializer(many=True, read_only=True)

    class Meta:
        model = Ride
        fields = "__all__"
    #     fields = [
    #     "id_ride",
    #     "status",
    #     "pickup_latitude",
    #     "pickup_longitude",
    #     "dropoff_latitude",
    #     "dropoff_longitude",
    #     "pickup_time",
    #     "rider",
    #     "driver",
    #     "todays_ride_events",
    #     "distance",  # annotated field
    # ]
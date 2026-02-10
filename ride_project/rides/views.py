from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Prefetch
from django.utils import timezone
from datetime import timedelta
from rest_framework.filters import OrderingFilter
from .models import Ride, RideEvent
from .serializers import RideSerializer
from .permissions import IsAdminRole
from .filters import RideFilter
from .services import annotate_distance
from .pagination import RidePagination
from rest_framework.decorators import action
from rest_framework.response import Response
from .reports import get_trip_duration_report
    

class RideViewSet(ModelViewSet):

    queryset = Ride.objects.all()     
    serializer_class = RideSerializer
    permission_classes = [IsAdminRole]

    filter_backends = [
        DjangoFilterBackend,
        OrderingFilter
    ]

    filterset_class = RideFilter
    pagination_class = RidePagination
    ordering_fields = ['pickup_time', 'distance']
    # filter_backends = [OrderingFilter]

    def get_queryset(self):

        last_24_hours = timezone.now() - timedelta(hours=24)

        events_qs = RideEvent.objects.filter(
            created_at__gte=last_24_hours
        )

        qs = Ride.objects.select_related(
            "id_rider", "id_driver"
        ).prefetch_related(
            Prefetch(
                "ride_events",
                queryset=events_qs,
                to_attr="todays_ride_events"
            )
        )

        lat = self.request.query_params.get("lat")
        lng = self.request.query_params.get("lng")

        if lat and lng:
            qs = annotate_distance(qs, float(lat), float(lng))

        return qs
    
    @action(detail=False, methods=["get"], url_path="trip-report")
    def trip_report(self, request):

        month = request.query_params.get("month")
        data = get_trip_duration_report(month=month)

        return Response(data)
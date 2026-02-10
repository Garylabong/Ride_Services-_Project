from django.db.models import F, FloatField, ExpressionWrapper
from django.db.models.functions import ACos, Cos, Sin, Radians


def annotate_distance(queryset, lat, lng):

    return queryset.annotate(
        distance=ExpressionWrapper(
            ACos(
                Sin(Radians(lat)) *
                Sin(Radians(F('pickup_latitude'))) +
                Cos(Radians(lat)) *
                Cos(Radians(F('pickup_latitude'))) *
                Cos(Radians(F('pickup_longitude') - lng))
            ) * 6371,
            output_field=FloatField()
        )
    )
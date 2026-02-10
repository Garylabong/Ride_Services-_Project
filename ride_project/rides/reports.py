# from django.db import connection


# def get_trip_duration_report():

#     query = f"""
#     WITH pickup_events AS (
#     SELECT
#         id_ride_id,
#         created_at AS pickup_time
#     FROM rides_rideevent
#     WHERE description = 'Status changed to pickup'
#     ),

#     dropoff_events AS (
#         SELECT
#             id_ride_id,
#             created_at AS dropoff_time
#         FROM rides_rideevent
#         WHERE description = 'Status changed to dropoff'
#     ),

#     trip_durations AS (
#         SELECT
#             r.id_driver_id,
#             p.id_ride_id,
#             p.pickup_time,
#             d.dropoff_time,
#             (julianday(d.dropoff_time) - julianday(p.pickup_time)) * 24 AS duration_hours
#         FROM pickup_events p
#         JOIN dropoff_events d
#             ON p.id_ride_id = d.id_ride_id
#         JOIN rides_ride r
#             ON r.id_ride = p.id_ride_id 
#     )

#     SELECT
#         strftime('%Y-%m', pickup_time) AS month,
#         u.first_name || ' ' || u.last_name AS driver,
#         COUNT(*) AS trips_over_1_hour
#     FROM trip_durations td
#     JOIN rides_user u
#         ON u.id_user = td.id_driver_id
#     WHERE duration_hours > 1
#     GROUP BY month, driver
#     ORDER BY month, driver;

#     """

#     with connection.cursor() as cursor:
#         cursor.execute(query)

#         columns = [col[0] for col in cursor.description]
#         rows = cursor.fetchall()

#     return [dict(zip(columns, row)) for row in rows]
from django.db import connection
from rides.models import Ride, RideEvent, User


def get_trip_duration_report(month=None):

    ride_table = Ride._meta.db_table
    event_table = RideEvent._meta.db_table
    user_table = User._meta.db_table

    month_filter = ""
    params = []

    if month:
        month_filter = "AND strftime('%Y-%m', pickup_time) = %s"
        params.append(month)

    query = f"""
    WITH pickup_events AS (
        SELECT id_ride_id, created_at AS pickup_time
        FROM {event_table}
        WHERE description = 'Status changed to pickup'
    ),

    dropoff_events AS (
        SELECT id_ride_id, created_at AS dropoff_time
        FROM {event_table}
        WHERE description = 'Status changed to dropoff'
    ),

    trip_durations AS (
        SELECT
            r.id_driver_id,
            p.id_ride_id,
            p.pickup_time,
            d.dropoff_time,
            (julianday(d.dropoff_time) - julianday(p.pickup_time)) * 24 AS duration_hours
        FROM pickup_events p
        JOIN dropoff_events d
            ON p.id_ride_id = d.id_ride_id
        JOIN {ride_table} r
            ON r.id_ride = p.id_ride_id
    )

    SELECT
        strftime('%Y-%m', pickup_time) AS month,
        u.first_name || ' ' || u.last_name AS driver,
        COUNT(*) AS trips_over_1_hour
    FROM trip_durations td
    JOIN {user_table} u
        ON u.id_user = td.id_driver_id
    WHERE duration_hours > 1
    {month_filter}
    GROUP BY month, driver
    ORDER BY month, driver;
    """

    with connection.cursor() as cursor:
        cursor.execute(query, params)
        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()

    return [dict(zip(columns, row)) for row in rows]

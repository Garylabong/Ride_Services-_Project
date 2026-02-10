# Ride_Services_Project

## Overview

This project is a RESTful API built with Django REST Framework for managing ride information.
It is optimized for performance and scalability, assuming very large Ride and RideEvent tables.

## Features

- Admin-only authenticated API access
- Ride listing with pagination
- Filtering by ride status and rider email
- Sorting by pickup time and distance from GPS coordinates
- Optimized retrieval of ride events (last 24 hours only)
- Minimal SQL queries (2–3 per request)
- Raw SQL reporting for trip duration analytics

---

## Tech Stack

- Python 3.4
- Django
- Django REST Framework
- PostgreSQL (recommended)

---

## Setup Instructions

### 1. Clone Repository

```bash
git clone https://github.com/Garylabong/Ride_Services_Project.git
cd Ride_Services_Project
```

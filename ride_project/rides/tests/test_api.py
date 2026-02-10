from rest_framework.test import APITestCase
from django.urls import reverse
from rides.models import User


class RideAPITest(APITestCase):

    def setUp(self):
        self.admin = User.objects.create_user(
            username="admin",
            password="pass123",
            role="admin"
        )

    def test_auth_required(self):
        response = self.client.get("/api/rides/")
        self.assertEqual(response.status_code, 403)

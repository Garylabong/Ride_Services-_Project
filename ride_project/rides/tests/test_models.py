from django.test import TestCase
from rides.models import User


class UserModelTest(TestCase):

    def test_create_user(self):
        user = User.objects.create(
            username="admin",
            role="admin"
        )

        self.assertEqual(user.role, "admin")

from django.test import Client
from django.test import TestCase


# Create your tests here.

# Test case for the method get not allowed.
class MethodGetNotAllowed(TestCase):

    def setUp(self):
        self.client = Client()

    def test_fibonacci_home_view(self):
        response = self.client.get("/users/")
        self.assertEqual(response.status_code, 405)


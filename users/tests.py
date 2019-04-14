from django.test import Client
from django.test import TestCase
from users.models import User

TEST_SUPER_USER_EMAIL = 'test@dummy.com'
TEST_SUPER_USER_PASSWORD = 'password@123'
TEST_SUPER_USER_FIRST_NAME = 'John'
TEST_SUPER_USER_LAST_NAME = 'Smith'


TEST_USER_EMAIL = 'testuser@dummy.com'
TEST_USER_PASSWORD = 'password@123'
TEST_USER_FIRST_NAME = 'John'
TEST_USER_LAST_NAME = 'Smith'


class UserModuleTest(TestCase):

    def setUp(self):
        self.client = Client()
        user = User.objects.create(email=TEST_SUPER_USER_EMAIL, first_name=TEST_SUPER_USER_LAST_NAME,
                                   last_name=TEST_SUPER_USER_FIRST_NAME,
                                   is_superuser=True)
        user.set_password(TEST_SUPER_USER_PASSWORD)
        user.save()

    def test_user_sign_up_get_not_allowed(self):
        response = self.client.get("/users/signup/")
        self.assertEqual(response.status_code, 405)

    def test_authentication_required(self):
        """Test case to check if authentication required for this view"""
        response = self.client.get("/users/list-users/")
        self.assertEqual(response.status_code, 401)

    def test_auth_successful(self):
        data = dict()
        data['username'] = TEST_SUPER_USER_EMAIL
        data['password'] = TEST_SUPER_USER_PASSWORD
        response = self.client.post("/api-token-auth/", data)
        self.assertEqual(response.status_code, 200)

    def test_signup_view(self):
        """Test to signup a user successfully via application"""
        data = dict()
        data['first_name'] = TEST_USER_FIRST_NAME
        data['last_name'] = TEST_USER_LAST_NAME
        data['email'] = TEST_USER_EMAIL
        data['password'] = TEST_USER_PASSWORD
        response = self.client.post("/users/signup/", data)
        self.assertEqual(response.status_code, 201)

    def test_sign_up_failview(self):
        print(User.objects.all())
        """Test Signup fail notice missing email from post body"""
        data = dict()
        data['first_name'] = TEST_USER_FIRST_NAME
        data['last_name'] = TEST_USER_LAST_NAME
        data['password'] = TEST_USER_PASSWORD
        response = self.client.post("/users/signup/", data)
        self.assertEqual(response.status_code, 400)

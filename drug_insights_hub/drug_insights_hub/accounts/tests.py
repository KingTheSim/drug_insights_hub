from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from drug_insights_hub.accounts.models import UserProfile

USER_MODEL = get_user_model()


class UserRegistrationViewTest(TestCase):
    def test_user_registration(self):
        username = "test_user"
        first_name = "first_name_test"
        last_name = "last_name_test"
        password = "password_test"

        response = self.client.post(
            reverse("register"),
            {
                "username": username,
                "first_name": first_name,
                "last_name": last_name,
                "password1": password,
                "password2": password,
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(USER_MODEL.objects.filter(username=username).exists())
        user = USER_MODEL.objects.get(username=username)

        self.assertTrue(UserProfile.objects.filter(user=user).exists())

    def test_signal_create_user_profile(self):
        user: User = USER_MODEL.objects.create_user(
            username="test_user",
            first_name="first_name_test",
            last_name="last_name_test",
            password="test_password",
        )
        self.assertTrue(UserProfile.objects.filter(user=user).exists())


class UserLoginViewTest(TestCase):
    def setUp(self):
        # Create a test user with valid credentials
        self.user = USER_MODEL.objects.create_user(
            username="test_user",
            first_name="first_name_test",
            last_name="last_name_test",
            password="test_password",
        )

    def test_login_success(self):
        response = self.client.post(
            reverse("login"), {"username": "test_user", "password": "test_password"}
        )
        self.assertRedirects(response, reverse("index"))

    def test_login_failure(self):
        response = self.client.post(
            reverse("login"),
            {"username": "invalid_user", "password": "invalid_password"},
        )
        self.assertContains(response, "Please enter a correct username and password.")

    def test_template_render(self):
        response = self.client.get(reverse("login"))
        self.assertTemplateUsed(response, "accounts/login.html")
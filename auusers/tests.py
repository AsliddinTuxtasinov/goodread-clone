from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
User = get_user_model()


class RegistrationCase(TestCase):

    def test_user_account_is_created(self):
        data_context = {
            'username': "asliddin",
            'first_name': "Asliddin",
            'last_name': "Tuxtasinov",
            'email': "asliddin@gmail.com",
            'password': "asliddin1!"
        }

        self.client.post(path=reverse('auusers:register'), data=data_context)
        user = User.objects.get(username=data_context['username'])

        self.assertEqual(first=user.first_name, second=data_context['first_name'])
        self.assertEqual(first=user.last_name, second=data_context['last_name'])
        self.assertEqual(first=user.email, second=data_context['email'])
        self.assertNotEqual(first=user.password, second=data_context['password'])
        self.assertTrue(user.check_password(data_context['password']))

    def test_required_field(self):
        data_context = {
            'first_name': "Asliddin",
            'email': "asliddin@gmail.com",
        }

        response = self.client.post(path=reverse('auusers:register'), data=data_context)
        user_count = User.objects.count()

        self.assertEqual(first=user_count, second=0)
        self.assertFormError(response=response, form="form", field="username", errors="This field is required.")
        self.assertFormError(response=response, form="form", field="password", errors="This field is required.")

    def test_invalid_email(self):
        data_context = {
            'username': "asliddin",
            'first_name': "Asliddin",
            'last_name': "Tuxtasinov",
            'email': "invalid-email",
            'password': "asliddin1!"
        }

        response = self.client.post(path=reverse('auusers:register'), data=data_context)
        user_count = User.objects.count()

        self.assertEqual(first=user_count, second=0)
        self.assertFormError(response=response, form="form", field="email", errors="Enter a valid email address.")

    def test_unique_username(self):
        data_context1 = {
            'username': "asliddin",
            'first_name': "Asliddin",
            'last_name': "Tuxtasinov",
            'email': "asliddin@gmail.com",
            'password': "asliddin1!"
        }
        data_context2 = {
            'username': "asliddin",
            'first_name': "Asliddinbek",
            'last_name': "Tuxtasinov",
            'email': "asliddin@gmail.com",
            'password': "asliddin1#"
        }
        self.client.post(path=reverse('auusers:register'), data=data_context1)
        response = self.client.post(path=reverse('auusers:register'), data=data_context2)

        self.assertFormError(response=response, form="form", field="username",
                             errors="A user with that username already exists.")

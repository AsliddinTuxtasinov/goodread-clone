from django.test import TestCase
from django.contrib.auth import get_user_model, get_user
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


class LoginTestCase(TestCase):

    def setUp(self) -> None:
        self.db_user = User.objects.create(username="asliddin", first_name="Asliddin",
                                           last_name="Tuxtasinov", email="asliddin@gmail.com")
        self.db_user.set_password("asliddin1!")
        self.db_user.save()

    def test_sucessful_login(self):
        user_count = User.objects.count()

        data = {'username': "asliddin", 'password': "asliddin1!"}
        self.client.post(path=reverse('auusers:login'), data=data)
        user = get_user(self.client)

        self.assertEqual(first=user_count, second=1)
        self.assertTrue(user.is_authenticated)

    def test_wrong_login(self):
        data = {'username': "wrong-username", 'password': "asliddin1!"}
        data2 = {'username': "asliddin", 'password': "wrong-password"}

        self.client.post(path=reverse('auusers:login'), data=data)
        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)

        self.client.post(path=reverse('auusers:login'), data=data2)
        user2 = get_user(self.client)
        self.assertFalse(user2.is_authenticated)

    def test_logout(self):
        data = {'username': "asliddin", 'password': "asliddin1!"}
        self.client.login(username=data['username'], password=data['password'])
        user = get_user(self.client)
        self.assertTrue(user.is_authenticated)

        self.client.get(path=reverse("auusers:logout"))
        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)


class ProfileTestCase(TestCase):

    def test_login_required(self):
        response = self.client.get(path=reverse("auusers:profile"))

        self.assertEqual(first=response.url, second=reverse("auusers:login")+"?next="+reverse("auusers:profile"))
        self.assertEqual(first=response.status_code, second=302)

    def test_profile_details(self):
        data_context = {
            'username': "asliddin",
            'first_name': "Asliddin",
            'last_name': "Tuxtasinov",
            'email': "asliddin@gmail.com",
            'password': "asliddin1!"
        }

        self.client.post(path=reverse('auusers:register'), data=data_context)
        user = User.objects.get(username=data_context['username'])

        self.assertNotEqual(first=user.password, second=data_context['password'])
        self.assertTrue(user.check_password(data_context['password']))

        self.client.login(username=data_context['username'], password=data_context['password'])

        response = self.client.get(path=reverse("auusers:profile"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, user.username)

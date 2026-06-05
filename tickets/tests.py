from django.test import Client, TestCase
from django.urls import reverse

from .models import Bus, Route, Trip
from .views import seed_data_if_empty


class TicketSmokeTests(TestCase):
    def setUp(self):
        seed_data_if_empty()
        self.client = Client()

    def test_public_trips_page_loads(self):
        response = self.client.get(reverse('trips'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Kampala')

    def test_staff_login_loads_dashboard(self):
        response = self.client.post(
            reverse('login'),
            {'email': 'admin@nts.ug', 'password': 'admin'},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Staff')

    def test_seed_data_creates_core_records(self):
        self.assertTrue(Bus.objects.exists())
        self.assertTrue(Route.objects.exists())
        self.assertTrue(Trip.objects.exists())

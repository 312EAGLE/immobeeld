from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from projects.models import Company,Customer


class HomePageTest(TestCase):
    def test_home_page_status_code(self):
        response = self.client.get(reverse('index.html'))
        self.assertEqual(response.status_code, 200)


class FotoPageTest(TestCase):
    def test_foto_page_status_code(self):
        response = self.client.get(reverse('foto.html'))
        self.assertEqual(response.status_code, 200)


class VideoPageTest(TestCase):
    def test_video_page_status_code(self):
        response = self.client.get(reverse('video.html'))
        self.assertEqual(response.status_code, 200)


class V360PageTest(TestCase):
    def test_v360_page_status_code(self):
        response = self.client.get(reverse('360.html'))
        self.assertEqual(response.status_code, 200)


class ContactPageTest(TestCase):
    def test_contact_page_status_code(self):
        response = self.client.get(reverse('contact.html'))
        self.assertEqual(response.status_code, 200)


class SignUpPageTest(TestCase):
    def test_sign_up_page_status_code(self):
        response = self.client.get(reverse('sign_up.html'))
        self.assertEqual(response.status_code, 200)


class LoginPageTest(TestCase):
    def test_login_page_status_code(self):
        response = self.client.get(reverse('login.html'))
        self.assertEqual(response.status_code, 200)


class LogoutPageTest(TestCase):
    def test_logout_page_status_code(self):
        response = self.client.get(reverse('logout.html'))
        self.assertEqual(response.status_code, 302)


class UpdateCustomerPageTest(TestCase):
    def test_update_customer_page_status_code(self):
        user = User.objects.create_user(username='customer2', password='SAMSUNg13*')
        self.client.login(username='customer2', password='SAMSUNg13*')
        response = self.client.get(reverse('update-customer'))
        self.assertEqual(response.status_code, 200)


class UpdateCompanyPageTest(TestCase):
    def test_update_company_page_status_code(self):
        user = User.objects.create_user(username='customer2', password='SAMSUNg13*')
        self.client.login(username='customer2', password='SAMSUNg13*')
        response = self.client.get(reverse('update-company'))
        self.assertEqual(response.status_code, 302)

class CreateOrderPageTest(TestCase):
    def test_create_order_page_status_code(self):
        user = User.objects.create_user(username='customer2', password='SAMSUNg13*')
        self.client.login(username='customer2', password='SAMSUNg13*')
        response = self.client.get(reverse('createorder.html'))
        self.assertEqual(response.status_code, 200)


class GetCompanyInfoPageTest(TestCase):
    def test_get_company_info_page_status_code(self):
        user = User.objects.create_user(username='customer2', password='SAMSUNg13*')
        self.client.login(username='customer2', password='SAMSUNg13*')
        response = self.client.get(reverse('company-info', kwargs={'company_id': 1}))
        self.assertEqual(response.status_code, 404)


class OrdersPageTest(TestCase):
    def test_orders_page_status_code(self):
        user = User.objects.create_user(username='customer2', password='SAMSUNg13*')
        self.client.login(username='customer2', password='SAMSUNg13*')

        # Check if a Customer object already exists for the user
        try:
            customer = Customer.objects.get(user=user)
        except Customer.DoesNotExist:
            # If it doesn't exist, create a new Customer object
            customer = Customer.objects.create(user=user)

        # Create a Company object associated with the Customer
        company = Company.objects.create(customer=customer)

        response = self.client.get(reverse('orders.html'))
        self.assertEqual(response.status_code, 200)


class DashboardPageTest(TestCase):
    def test_dashboard_page_status_code(self):
        user = User.objects.create_user(username='customer2', password='SAMSUNg13*')
        self.client.login(username='customer2', password='SAMSUNg13*')

        # Check if a Customer object already exists for the user
        try:
            customer = Customer.objects.get(user=user)
        except Customer.DoesNotExist:
            # If it doesn't exist, create a new Customer object
            customer = Customer.objects.create(user=user)

        # Create a Company object associated with the Customer
        company = Company.objects.create(customer=customer)


        response = self.client.get(reverse('dashboard.html'))
        self.assertEqual(response.status_code, 200)

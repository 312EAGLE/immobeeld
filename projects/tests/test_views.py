from django.test import TestCase, Client , RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User, Group
from projects.models import *
from django.http import HttpResponse
from projects.views import *
import uuid
from django.contrib.messages import get_messages
from decimal import Decimal

class DashboardViewTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='customer2', password='SAMSUNg13*')
        cls.customer, _ = Customer.objects.get_or_create(user=cls.user)
        cls.company, _ = Company.objects.get_or_create(customer=cls.customer)
        cls.url = reverse('dashboard.html')

    def test_dashboard_view_with_authenticated_user(self):
        self.client.login(username='customer2', password='SAMSUNg13*')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard.html')
        self.assertContains(response, 'Dashboard')

    def test_dashboard_view_with_unauthenticated_user(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, '/login/?next=/dashboard/')

class HomeViewTest(TestCase):
    def test_home_view(self):
        url = reverse('index.html') 
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
        
class FotoViewTest(TestCase):
    def test_foto_view(self):
        url = reverse('foto.html')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'foto.html')

class VideoViewTest(TestCase):
    def test_video_view(self):
        url = reverse('video.html')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'video.html')

class V360ViewTest(TestCase):
    def test_v360_view(self):
        url = reverse('360.html')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, '360.html')

class ContactViewTest(TestCase):
    def test_contact_view(self):
        url = reverse('contact.html')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contact.html')

class RegisterViewTest(TestCase):
    def test_register_view(self):
        url = reverse('sign_up.html')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sign_up.html')
        

class UserLoginViewTest(TestCase):
    def test_user_login_view(self):
        url = reverse('login.html')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')


class UserLogoutViewTest(TestCase):
    def test_user_logout_view(self):
        url = reverse('logout.html')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/')

class OrdersViewTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='customer2', password='SAMSUNg13*')
        cls.customer, _ = Customer.objects.get_or_create(user=cls.user)
        cls.company, _ = Company.objects.get_or_create(customer=cls.customer)
        cls.url = reverse('orders.html')

    def test_orders_view_with_authenticated_user(self):
        self.client.login(username='customer2', password='SAMSUNg13*')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'orders.html')
        

    def test_orders_view_with_unauthenticated_user(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, '/login/?next=/orders/')


'''class CreateOrderViewTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='customer2', password='SAMSUNg13*')
        cls.url = reverse('createorder.html')

    def test_create_order_view_with_authenticated_user(self):
        self.client.login(username='customer2', password='SAMSUNg13*')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'createorder.html')
        

    def test_create_order_view_with_unauthenticated_user(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, '/login/?next=/createorder')'''

class GetCompanyInfoViewTest(TestCase):
    def test_get_company_info_view(self):
        company = Company.objects.create(companyname='Test Company', vat='1234567890')
        url = reverse('company-info', args=[company.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 302)

class DownloadOrdersTest(TestCase):
    
    def setUp(self):
        # Create a unique username using uuid
        unique_username = f'jacob{uuid.uuid4()}'
        self.user = User.objects.create_user(username=unique_username, email='jacob@test.com', password='top_secret')

        # Use get_or_create to avoid IntegrityError
        self.customer, created = Customer.objects.get_or_create(user=self.user,
                                                                defaults={'name': 'Jacob',
                                                                          'prefix': 'Mr.',
                                                                          'familyname': 'Kaplan',
                                                                          'phone': '1234567890',
                                                                          'email': 'jacob@test.com'})
        ...

        # Create required related objects
        self.status = Status.objects.create(status='Test Status')
        self.order_type = OrderType.objects.create(type_name='Test OrderType')
        self.country = Country.objects.create(country='Test Country')
        self.key_choice = KeyChoice.objects.create(key_choice='Test KeyChoice')
        self.get_keys_choice = GetKeysChoice.objects.create(get_keys_choice='Test GetKeysChoice')
        self.get_keys_language = GetKeysLanguage.objects.create(get_keys_language='Test Language')

        # Create a Service
        self.service = Service.objects.create(service_name='Test Service')

        # Create an Order
        self.order = Order.objects.create(
            customer=self.customer, 
            status=self.status,
            type=self.order_type,
            country=self.country,
            straatnaam="Test Street",
            huisnummer="123",
            postcode="1234 AB",
            plaats="Test Place",
            gebruiksoppervlakte=100.00,
            oppervlakteBijgebouwen=50.00,
            perceel=150.00,
            keys=self.key_choice,
            get_keys=self.get_keys_choice,
            get_keys_name="Test GetKeysName",
            get_keys_phone="123456789",
            get_keys_email="testgetkeys@example.com",
            get_keys_adr="Test GetKeysAddress",
            get_keys_zip="1234 AB",
            get_keys_city="Test GetKeysCity",
            get_keys_language=self.get_keys_language,
            inv_name="Test InvoiceName",
            inv_vat="Test VAT",
            inv_adr="Test InvoiceAddress",
            inv_zip="1234 AB",
            inv_city="Test InvoiceCity",
            inv_country="Test Country",
            inv_phone="123456789",
            inv_email="testinvoice@example.com",
            rec_email="testrecipient@example.com",
            rec_email_owner="testowner@example.com",
            rec_email_other="testother@example.com"
        )
        
        # Add the service to the order
        self.order.services.add(self.service)

        self.factory = RequestFactory()
        
    def test_download_orders(self):
        # Create a request
        request = self.factory.get('download_orders/')
        
        # Attach the user to the request
        request.user = self.user
        
        # Call the view
        response = download_orders(request)
        
        # Check that the response has the correct content type
        self.assertEqual(response['Content-Type'], 'text/csv')
        
        # Check that the response contains the order
        # We'll just check for the order ID, for simplicity
        self.assertIn(str(self.order.id), str(response.content))


class TestCreateOrderView(TestCase):
    def setUp(self):
        """Set up for the tests."""
        self.client = Client()
        self.url = reverse('createorder.html')
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.user.save()

        # we dont need to create customer because its alreaedy created in register view. But double check
        if hasattr(self.user, 'customer'):
            self.customer = self.user.customer
        else:
            self.customer = Customer.objects.create(user=self.user)

        # Create necessary instances
        self.order_type = OrderType.objects.create(type_name='test_type')
        self.country = Country.objects.create(country='test_country')
        self.key_choice = KeyChoice.objects.create(key_choice='test_key_choice')
        self.get_keys_choice = GetKeysChoice.objects.create(get_keys_choice='test_get_keys_choice')
        self.invoice_recipient = InvoiceRecipient.objects.create(recipient='test_invoice_recipient')
        self.delivery_recipient = DeliveryRecipient.objects.create(recipient='test_delivery_recipient')
        self.service = Service.objects.create(service_name='test_service', price=100)
        self.get_keys_language = GetKeysLanguage.objects.create(get_keys_language='Test Language')

    def test_create_order_POST(self):
        """Test the POST method."""
        self.client.login(username='testuser', password='testpass')

        post_data = {
            'type': self.order_type.id,
            'straatnaam': 'Test Street',
            'huisnummer': '123',
            'toevoeging': 'Test Addition',
            'postcode': '12345',
            'plaats': 'Test Place',
            'gebruiksoppervlakte': Decimal('100'),
            'oppervlakteBijgebouwen': '50',
            'perceel': '200',
            'country': self.country.id,
            'keys': self.key_choice.id,
            'get_keys': self.get_keys_choice.id,
            'delivery_recipient': [self.delivery_recipient.id],  # for multiple choice field
            'invoice_recipient': self.invoice_recipient.id,
            'cost_reference': 'Test reference',
            'get_keys_name': 'Test Name',
            'get_keys_phone': '123456789',
            'get_keys_email': 'test@test.com',
            'get_keys_adr': 'Test Address',
            'get_keys_zip': '12345',
            'get_keys_city': 'Test City',
            'get_keys_language': self.get_keys_language.id,
            'inv_name': 'Test Invoice Name',
            'inv_vat': 'Test VAT',
            'inv_adr': 'Test Invoice Address',
            'inv_zip': '12345',
            'inv_city': 'Test Invoice City',
            'inv_country': 'Test Country',
            'inv_phone': '123456789',
            'inv_email': 'testinvoice@test.com',
            'rec_email': 'testreceipt@test.com',
            'rec_email_owner': 'testreceiptowner@test.com',
            'rec_email_other': 'testreceiptother@test.com',
            'services': [self.service.id]  # for multiple choice field
        }

        response = self.client.post(self.url, post_data)

        # Check that the order was created
        self.assertEqual(Order.objects.count(), 1)

        # Retrieve the created order and check its fields
        order = Order.objects.first()

        # Now you can check all fields as you did
        self.assertEqual(order.type.id, post_data['type'])
        self.assertEqual(order.straatnaam, post_data['straatnaam'])
        self.assertEqual(order.huisnummer, post_data['huisnummer'])
        self.assertEqual(order.toevoeging, post_data['toevoeging'])
        self.assertEqual(order.postcode, post_data['postcode'])
        self.assertEqual(order.plaats, post_data['plaats'])
        self.assertEqual(order.gebruiksoppervlakte, post_data['gebruiksoppervlakte'])
        self.assertEqual(order.oppervlakteBijgebouwen, Decimal(post_data['oppervlakteBijgebouwen']))
        self.assertEqual(order.perceel, Decimal(post_data['perceel']))
        self.assertEqual(order.country.id, post_data['country'])
        self.assertEqual(order.keys.id, post_data['keys'])
        self.assertEqual(order.get_keys.id, post_data['get_keys'])
        self.assertEqual(order.cost_reference, post_data['cost_reference'])
        self.assertEqual(order.get_keys_name, post_data['get_keys_name'])
        self.assertEqual(order.get_keys_phone, post_data['get_keys_phone'])
        self.assertEqual(order.get_keys_email, post_data['get_keys_email'])
        self.assertEqual(order.get_keys_adr, post_data['get_keys_adr'])
        self.assertEqual(order.get_keys_zip, post_data['get_keys_zip'])
        self.assertEqual(order.get_keys_city, post_data['get_keys_city'])
        self.assertEqual(order.get_keys_language.id, post_data['get_keys_language'])
        self.assertEqual(order.inv_name, post_data['inv_name'])
        self.assertEqual(order.inv_vat, post_data['inv_vat'])
        self.assertEqual(order.inv_adr, post_data['inv_adr'])
        self.assertEqual(order.inv_zip, post_data['inv_zip'])
        self.assertEqual(order.inv_city, post_data['inv_city'])
        self.assertEqual(order.inv_country, post_data['inv_country'])
        self.assertEqual(order.inv_phone, post_data['inv_phone'])
        self.assertEqual(order.inv_email, post_data['inv_email'])
        self.assertEqual(order.rec_email, post_data['rec_email'])
        self.assertEqual(order.rec_email_owner, post_data['rec_email_owner'])
        self.assertEqual(order.rec_email_other, post_data['rec_email_other'])

        # Check for many-to-many field
        self.assertEqual(list(order.services.all()), [self.service])

        # Check that the response redirected to the right URL
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')

    '''def test_create_order_invalid_POST(self):
        """Test the POST method with invalid input."""
        self.client.login(username='testuser', password='testpass')

        response = self.client.post(self.url, {})

        # Check that the order was not created
        self.assertEqual(Order.objects.count(), 0)

        # Check that the response was a success
        self.assertEqual(response.status_code, 200)

        # Check that the error message was added
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Invalid form submission.')'''
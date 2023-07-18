from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    prefix = models.CharField(max_length=200, null=True, blank=True)
    familyname = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=200, null=True)
    

    def __str__(self):
        return str(self.name) if self.name else 'Unnamed Customer'

class OrderType(models.Model):
    type_name = models.CharField(max_length=100)

    def __str__(self):
        return self.type_name

class KeyChoice(models.Model):
    key_choice = models.CharField(max_length=50)

    def __str__(self):
        return self.key_choice

class GetKeysChoice(models.Model):
    get_keys_choice = models.CharField(max_length=50)

    def __str__(self):
        return self.get_keys_choice

class DeliveryRecipient(models.Model):
    recipient = models.CharField(max_length=50)


    def __str__(self):
        return self.recipient

class InvoiceRecipient(models.Model):
    recipient = models.CharField(max_length=50)


    def __str__(self):
        return self.recipient

class Status(models.Model):
    status = models.CharField(max_length=50)

    def __str__(self):
        return self.status

class Service(models.Model):
    service_name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2 , null=True)
    is_selected = models.BooleanField(default=False)

    def __str__(self):
        return self.service_name

class GetKeysLanguage(models.Model):
    get_keys_language = models.CharField(max_length=50)

    def __str__(self):
        return self.get_keys_language
    
class Country(models.Model):
    country = models.CharField(max_length=50)

    def __str__(self):
        return self.country

class InvCountry(models.Model):
    inv_country = models.CharField(max_length=50)

    def __str__(self):
        return self.inv_country

class Company(models.Model):
    
    #fk's
    get_keys_language =  models.ForeignKey(GetKeysLanguage, on_delete=models.CASCADE, null=True)
    country =  models.ForeignKey(Country, on_delete=models.CASCADE, null=True)
    customer = models.ForeignKey(Customer, null=True, on_delete= models.SET_NULL)
    

    companyname = models.CharField(max_length=200, null=True)
    vat = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=200, null=True)
    address = models.CharField(max_length=200, null=True)
    zip = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    
    
    billing_company_name = models.CharField(max_length=200, null=True)
    billing_vat = models.CharField(max_length=200, null=True)
    billing_adr = models.CharField(max_length=200, null=True)
    billing_zip = models.CharField(max_length=200, null=True)
    billing_city = models.CharField(max_length=200, null=True)
    billing_country = models.CharField(max_length=200, null=True)
    billing_email = models.EmailField(max_length=200, null=True)

    

    def __str__(self):
        return self.companyname if self.companyname else 'Unnamed Company'
    

class Order(models.Model):

    
    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    status = models.ForeignKey(Status, on_delete=models.CASCADE,null=True)


    #step 1
    type = models.ForeignKey(OrderType, on_delete=models.CASCADE)
    country =  models.ForeignKey(Country, on_delete=models.CASCADE, null=True)
    straatnaam = models.CharField(max_length=100)
    huisnummer = models.CharField(max_length=10)
    toevoeging = models.CharField(max_length=50, blank=True)
    postcode = models.CharField(max_length=20)
    plaats = models.CharField(max_length=50)
    gebruiksoppervlakte = models.DecimalField(max_digits=10, decimal_places=2)
    oppervlakteBijgebouwen = models.DecimalField(max_digits=10, decimal_places=2)
    perceel = models.DecimalField(max_digits=10, decimal_places=2)
    keys = models.ForeignKey(KeyChoice, on_delete=models.CASCADE, null=True)

    #step 2 
    cost_reference = models.CharField(max_length=100, blank=True, null=True)
    services = models.ManyToManyField(Service)
    total_excl_vat = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    total_incl_vat = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)


    # step 3

    get_keys = models.ForeignKey(GetKeysChoice, on_delete=models.CASCADE, null=True)
    delivery_recipient = models.ManyToManyField(DeliveryRecipient)
    invoice_recipient = models.ForeignKey(InvoiceRecipient, on_delete=models.CASCADE, null=True)
    
    
    #Step4

    # Get keys / Sleutel Ophaling
    get_keys_name = models.CharField(max_length=100,blank=True)
    get_keys_phone = models.CharField(max_length=100,blank=True)
    get_keys_email = models.CharField(max_length=100,blank=True)
    get_keys_adr = models.CharField(max_length=100,blank=True)
    get_keys_zip = models.CharField(max_length=100,blank=True)
    get_keys_city = models.CharField(max_length=100,blank=True)
    get_keys_language =  models.ForeignKey(GetKeysLanguage, on_delete=models.CASCADE, null=True)

    
    # Facturatie 
    inv_name = models.CharField(max_length=100,blank=True)
    inv_vat = models.CharField(max_length=100,blank=True)
    inv_adr = models.CharField(max_length=100,blank=True)
    inv_zip = models.CharField(max_length=100,blank=True)
    inv_city = models.CharField(max_length=100,blank=True)
    inv_country = models.CharField(max_length=100,blank=True,null=True)
    inv_phone = models.CharField(max_length=100,blank=True)
    inv_email = models.CharField(max_length=100,blank=True)       
    
    # Opleveren bestanden
    rec_email = models.CharField(max_length=100,blank=True)
    rec_email_owner = models.CharField(max_length=100,blank=True)
    rec_email_other = models.CharField(max_length=100,blank=True)

    def __str__(self):
        return f"Order {self.id}"



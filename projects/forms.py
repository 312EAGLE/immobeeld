from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django import forms
from django.contrib.auth.models import User
from decimal import Decimal
from .models import Order, Company, Customer , Service


class CreateUserForm(UserCreationForm):
    """Form for user registration."""
    companyname = forms.CharField(max_length=200)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'companyname']

class OrderForm(forms.ModelForm):
    """Form for creating an order."""
    def __init__(self, *args, user=None, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)

        # Get the customer for this user
        customer = Customer.objects.get(user=user)

        # Get the companies for this customer
        companies = Company.objects.filter(customer=customer)

        # Check if the company exists and retrieve the company data
        if companies.exists():
            company = companies[0]
            company_name = company.companyname
            company_phone = company.phone
            company_email = company.email
            company_address = company.address
            company_zip = company.zip
            company_city = company.city
            get_keys_language = company.get_keys_language
            country = company.country
            vat = company.vat
        else:
            company_name = ""
            company_phone = ""
            company_email = ""
            company_address = ""
            company_zip = ""
            company_city = ""
            get_keys_language = ""
            country = ""
            vat = ""

        # Set the widget and initial value for each field / autofillment
        self.fields['country'].initial = country.id if country else None

        # GET KEYS
        self.fields['get_keys_name'].widget = forms.TextInput(attrs={'class': 'form-control', 'value': company_name})
        self.fields['get_keys_phone'].widget = forms.TextInput(attrs={'class': 'form-control', 'value': company_phone})
        self.fields['get_keys_email'].widget = forms.TextInput(attrs={'class': 'form-control', 'value': company_email})
        self.fields['get_keys_adr'].widget = forms.TextInput(attrs={'class': 'form-control', 'value': company_address})
        self.fields['get_keys_zip'].widget = forms.TextInput(attrs={'class': 'form-control', 'value': company_zip})
        self.fields['get_keys_city'].widget = forms.TextInput(attrs={'class': 'form-control', 'value': company_city})
        # dropdown - select
        self.fields['get_keys_language'].initial = get_keys_language.id if get_keys_language else None

        # file receiver
        self.fields['rec_email'].widget = forms.TextInput(attrs={'class': 'form-control', 'value': company_email})

        # INVOICE / facturatie

        # invoice company name
        self.fields['inv_name'].widget = forms.TextInput(attrs={'class': 'form-control', 'value': company_name})
        # invoice vat number
        self.fields['inv_vat'].widget = forms.TextInput(attrs={'class': 'form-control', 'value': vat})

        # invoice addresss
        self.fields['inv_adr'].widget = forms.TextInput(attrs={'class': 'form-control', 'value': company_address})
        # invoice zip
        self.fields['inv_zip'].widget = forms.TextInput(attrs={'class': 'form-control', 'value': company_zip})
        # invoice zip
        self.fields['inv_city'].widget = forms.TextInput(attrs={'class': 'form-control', 'value': company_city})
        # invoice country
        self.fields['inv_country'].widget = forms.TextInput(attrs={'class': 'form-control', 'value': country})

        # invoice phone
        self.fields['inv_phone'].widget = forms.TextInput(attrs={'class': 'form-control', 'value': company_phone})
        # invoice email
        self.fields['inv_email'].widget = forms.TextInput(attrs={'class': 'form-control', 'value': company_email})

    services = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        queryset=Service.objects.all(),
        required=False,
    )

    def save(self, commit=True):
        instance = super().save(commit=False)

        total_excl_vat = sum(service.price for service in self.cleaned_data.get('services', []))
        total_incl_vat = total_excl_vat * Decimal('1.21')  # Add 21% VAT

        instance.total_excl_vat = total_excl_vat
        instance.total_incl_vat = total_incl_vat

        if commit:
            instance.save()
            instance.services.set(self.cleaned_data.get('services', []))

        return instance
    
    class Meta:
        model = Order
        fields = [
            # step1
            'type', 'straatnaam', 'huisnummer', 'toevoeging',
            'postcode', 'plaats', 'gebruiksoppervlakte', 'oppervlakteBijgebouwen',
            'perceel', 'country',
            # step2
            
            # step3
            'keys', 'get_keys', 'delivery_recipient',
            'invoice_recipient', 'cost_reference',
            # step4
            'get_keys_name', 'get_keys_phone',
            'get_keys_email', 'get_keys_adr', 'get_keys_zip', 'get_keys_city', 'get_keys_language',
            'inv_name', 'inv_vat', 'inv_adr', 'inv_zip', 'inv_city', 'inv_country', 'inv_phone', 'inv_email',
            'rec_email', 'rec_email_owner', 'rec_email_other'
        ]

        widgets = {
            # CONNECTING JINJA TO CSS
            # step 1
            'type': forms.Select(attrs={'class': 'form-select'}),
            'country': forms.Select(attrs={'class': 'form-select'}),
            'straatnaam': forms.TextInput(attrs={'class': 'form-control'}),
            'huisnummer': forms.TextInput(attrs={'class': 'form-control'}),
            'toevoeging': forms.TextInput(attrs={'class': 'form-control'}),
            'postcode': forms.TextInput(attrs={'class': 'form-control'}),
            'plaats': forms.TextInput(attrs={'class': 'form-control'}),
            'gebruiksoppervlakte': forms.TextInput(attrs={'class': 'form-control'}),
            'oppervlakteBijgebouwen': forms.TextInput(attrs={'class': 'form-control'}),
            'perceel': forms.TextInput(attrs={'class': 'form-control'}),

            # step2
            

            # step3check-form-group
            'keys': forms.Select(attrs={'class': 'form-select'}),
            'get_keys': forms.RadioSelect(attrs={'class': 'form-check-input'}),
            'delivery_recipient': forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
            'invoice_recipient': forms.RadioSelect(attrs={'class': 'form-check-input'}),
            'cost_reference': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'z.B. ABC123'}),

            # step4 '
            # getkeys:
            'get_keys_name': forms.TextInput(attrs={'class': 'form-control'}),
            'get_keys_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'get_keys_email': forms.TextInput(attrs={'class': 'form-control'}),
            'get_keys_adr': forms.TextInput(attrs={'class': 'form-control'}),
            'get_keys_zip': forms.TextInput(attrs={'class': 'form-control'}),
            'get_keys_city': forms.TextInput(attrs={'class': 'form-control'}),
            'get_keys_language': forms.Select(attrs={'class': 'form-select'}),

            # files receiver
            'rec_email': forms.TextInput(attrs={'class': 'form-control'}),
            'rec_email_owner': forms.TextInput(attrs={'class': 'form-control'}),
            'rec_email_other': forms.TextInput(attrs={'class': 'form-control'}),

            # getinvoice
            'inv_name': forms.TextInput(attrs={'class': 'form-control'}),
            'inv_vat': forms.TextInput(attrs={'class': 'form-control'}),
            'inv_adr': forms.TextInput(attrs={'class': 'form-control'}),
            'inv_zip': forms.TextInput(attrs={'class': 'form-control'}),
            'inv_city': forms.TextInput(attrs={'class': 'form-control'}),
            'inv_country': forms.Select(attrs={'class': 'form-select'}),
            'inv_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'inv_email': forms.TextInput(attrs={'class': 'form-control'}),
        }

    


class CompanyForm(forms.ModelForm):
    """Form for updating company information."""
    class Meta:
        model = Company
        fields = ['get_keys_language', 'country', 'companyname', 'vat', 'phone', 'email', 'address', 'zip', 'city',

                  # billing
                  'billing_company_name',
                  'billing_vat',
                  'billing_adr',
                  'billing_zip',
                  'billing_city',
                  'billing_country',
                  'billing_email']

        widgets = {
            'get_keys_language': forms.Select(attrs={'class': 'form-select'}),
            'country': forms.Select(attrs={'class': 'form-select'}),

            'companyname': forms.TextInput(attrs={'class': 'form-control'}),
            'vat': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'zip': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            # billing
            'billing_company_name': forms.TextInput(attrs={'class': 'form-control'}),
            'billing_vat': forms.TextInput(attrs={'class': 'form-control'}),
            'billing_adr': forms.TextInput(attrs={'class': 'form-control'}),
            'billing_zip': forms.TextInput(attrs={'class': 'form-control'}),
            'billing_city': forms.TextInput(attrs={'class': 'form-control'}),
            'billing_country': forms.TextInput(attrs={'class': 'form-control'}),
            'billing_email': forms.TextInput(attrs={'class': 'form-control'}),
        }


class CustomerForm(forms.ModelForm):
    """Form for updating customer information."""
    class Meta:
        model = Customer
        fields = ['name', 'prefix', 'familyname', 'phone', 'email']
        widgets = {
            # CONNECTING JINJA TO CSS
            # Customer
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'prefix': forms.TextInput(attrs={'class': 'form-control'}),
            'familyname': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
        }


class PasswordChangingForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder': 'Current Password'}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder': 'New Password'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder': 'Confirm New Password'}))

    class Meta:
        fields = ('old_password', 'new_password1', 'new_password2')

from django.shortcuts import render, redirect
from urllib import request
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group

from .forms import CreateUserForm, OrderForm, CompanyForm, CustomerForm , PasswordChangingForm

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages

from django.contrib.auth import authenticate, login as auth_login, logout , update_session_auth_hash
from .decorators import unauthenticated_user, allowed_users
from .models import Order, Customer, Company, DeliveryRecipient, InvoiceRecipient ,GetKeysChoice , Service
from django.http import HttpRequest, JsonResponse,Http404
from django.shortcuts import get_object_or_404
from typing import Any


import csv
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

def home(request):
    """Render the home page."""
    return render(request, 'index.html')


def foto(request):
    """Render the foto page."""
    return render(request, 'foto.html')


def video(request):
    """Render the video page."""
    return render(request, 'video.html')


def v360(request):
    """Render the 360 page."""
    return render(request, '360.html')


def contact(request):
    """Render the contact page."""
    return render(request, 'contact.html')


@unauthenticated_user
def register(request):
    """Handle user registration."""
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            companyname = form.cleaned_data.get('companyname')

            # Create customer for user
            if not hasattr(user, 'customer'):
                customer = Customer.objects.create(user=user, email=email)
            else:
                customer = user.customer
                customer.email = email
                customer.save()

            group = Group.objects.get(name='customer')
            user.groups.add(group)

            messages.success(request, 'Your account has successfully registered! ' + username)

            # Create company and set delivery_recipient and invoice_recipient
            company = Company.objects.create(customer=customer, companyname=companyname)
           
            return redirect('login.html')

    context = {'form': form}
    return render(request, 'sign_up.html', context)


@unauthenticated_user
def user_login(request):
    """Handle user login."""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            return redirect('dashboard.html')
        else:
            messages.info(request, 'Username or Password are incorrect!')

    context = {}
    return render(request, 'login.html', context)


def user_logout(request):
    """Handle user logout."""
    logout(request)
    return redirect('login.html')


@login_required(login_url='login.html')
@allowed_users(allowed_roles=['admin', 'customer'])
def dashboard(request):
    """Render the dashboard page."""
    # Retrieve customer and company objects
    try:
        customer = Customer.objects.get(user=request.user)
        company = Company.objects.get(customer=customer)
    except Customer.DoesNotExist:
        customer = None
        company = None

    # Create forms and populate them with existing data
    customer_form = CustomerForm(instance=customer)
    company_form = CompanyForm(instance=company)

    context = {
        'customer': customer,
        'company': company,
        'customer_form': customer_form,
        'company_form': company_form
    }

    return render(request, 'dashboard.html', context)

@login_required(login_url='login.html')
@allowed_users(allowed_roles=['admin', 'customer'])
def update_customer(request: HttpRequest) -> Any:
    """Handle update of customer information."""
    try:
        customer = Customer.objects.get(user=request.user)
        password_form = PasswordChangingForm(request.user, request.POST or None)
        if request.method == 'POST':
            form = CustomerForm(request.POST, instance=customer)
            if form.is_valid() and password_form.is_valid():
                form.save()
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Your profile and password were successfully updated!')
                return redirect('/dashboard')
            elif form.is_valid():
                form.save()
                messages.success(request, 'Your profile was successfully updated!')
                return redirect('/dashboard')
            elif password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Your password was successfully updated!')
                return redirect('/dashboard')
            else:
                messages.error(request, 'Please correct the error below.')
        else:
            form = CustomerForm(instance=customer)
    except Customer.DoesNotExist:
        return redirect('/dashboard')  
    except Exception as e:
        # Log the error message and handle the exception here
        print(str(e))

    return render(request, 'dashboard.html', {'customer_form': form, 'customer': customer, 'password_form': password_form})


@login_required(login_url='login.html')
@allowed_users(allowed_roles=['admin', 'customer'])
def update_company(request):
    """Handle update of company information."""
    try:
        customer = Customer.objects.get(user=request.user)
        company = Company.objects.get(customer=customer)
    except (Customer.DoesNotExist, Company.DoesNotExist):
        return redirect('/dashboard')  # Redirect to dashboard if customer or company doesn't exist

    if request.method == 'POST':
        form = CompanyForm(request.POST, instance=company)
        if form.is_valid():
            form.save()
            print('COMPANY information has been updated!')
            return redirect('/dashboard')
    else:
        form = CompanyForm(instance=company)

    return render(request, 'dashboard.html', {'company_form': form, 'company': company})

@login_required(login_url='login.html')
@allowed_users(allowed_roles=['admin', 'customer'])
def orders(request):
    """Render the orders page."""
    try:
        customer = Customer.objects.get(user=request.user)
        company = Company.objects.get(customer=customer)
    except Customer.DoesNotExist:
        customer = None
        company = None
    # Create forms and populate them with existing data
   
    # If the customer exists, get their orders, else get no orders
    orders = Order.objects.filter(customer=customer) if customer else Order.objects.none()

    context = {
        'customer': customer,
        'orders': orders,
        'company': company,
    }
    
   
    return render(request, 'orders.html',context)


@login_required(login_url='login.html')
@allowed_users(allowed_roles=['admin', 'customer'])
def createOrder(request):
    """Handle the creation of an order."""
    services = Service.objects.all()  # Get all services from the database

    if request.method == 'POST':
        form = OrderForm(request.POST, user=request.user)
        
        if form.is_valid():
            order = form.save(commit=False)
            try:
                order.customer = Customer.objects.get(user=request.user)
            except Customer.DoesNotExist:
                return render(request, 'error.html', {'message': 'Customer does not exist.'})

            order.save()  # Save the Order instance before adding services
            
            # Now add the selected services to the order
            selected_services = request.POST.getlist('services')  # This is a list of the ids of the selected services
            services = Service.objects.filter(id__in=selected_services)  # Get the Service instances
            order.services.set(services)  # Add the services to the order
            order.save()  # Save the Order instance again after adding services

            return redirect('orders.html')
        else:
            print(form.errors)  # Print form errors if form is not valid
    else:
        form = OrderForm(user=request.user)

    return render(request, 'createorder.html', {'form': form, 'services': services})  # Pass services to the template


@login_required(login_url='login.html')
@allowed_users(allowed_roles=['admin', 'customer'])
def get_company_info(request, company_id):
    """Retrieve company information using company ID and return as JSON response."""
    company = get_object_or_404(Company, id=company_id)
    data = {
        'company_name': company.companyname,
        'vat': company.vat,
        'phone': company.phone,
        'email': company.email,
        'address': company.address,
        'zip': company.zip,
        'city': company.city,
        'country': company.country,
    }
    return JsonResponse(data)



@login_required(login_url='login.html')
@allowed_users(allowed_roles=['admin', 'customer'])
def download_orders(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="orders.csv"'

    
    writer = csv.writer(response, delimiter=';')

    # Header row
    writer.writerow(['ID', 'Customer', 'Date Created', 'Status', 'Order Type', 'Country', 'Straatnaam', 'Huisnummer',
                    'Toevoeging', 'Postcode', 'Plaats', 'Gebruiksoppervlakte', 'OppervlakteBijgebouwen', 'Perceel',
                    'Keys', 'Cost Reference', 'Total excl VAT', 'Total incl VAT', 'Get Keys', 
                    'Get Keys Name', 'Get Keys Phone', 'Get Keys Email', 'Get Keys Address', 'Get Keys ZIP', 
                    'Get Keys City', 'Get Keys Language', 'Invoice Name', 'Invoice VAT', 'Invoice Address', 
                    'Invoice ZIP', 'Invoice City', 'Invoice Country', 'Invoice Phone', 'Invoice Email', 
                    'Recipient Email', 'Recipient Email Owner', 'Recipient Email Other'])

    orders = Order.objects.all()
    for order in orders:
        try:
            
            services = ', '.join(str(service) for service in order.services.all())
            writer.writerow([order.id, order.customer, order.date_created, order.status, order.type, order.country,
                            order.straatnaam, order.huisnummer, order.toevoeging, order.postcode, order.plaats,
                            order.gebruiksoppervlakte, order.oppervlakteBijgebouwen, order.perceel, order.keys,
                            order.cost_reference, order.total_excl_vat, order.total_incl_vat, order.get_keys,
                            order.get_keys_name, order.get_keys_phone, order.get_keys_email, order.get_keys_adr,
                            order.get_keys_zip, order.get_keys_city, order.get_keys_language, order.inv_name,
                            order.inv_vat, order.inv_adr, order.inv_zip, order.inv_city, order.inv_country, order.inv_phone,
                            order.inv_email, order.rec_email, order.rec_email_owner, order.rec_email_other])
        except Exception as e:
            print(str(e))  # Print the error message
            continue  # Skip to the next order if there's an error

    return response
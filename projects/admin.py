from django.contrib import admin
from .models import *

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'display_services', 'total_excl_vat', 'total_incl_vat')

    def display_services(self, obj):
        return ", ".join([service.service_name for service in obj.services.all()])

    display_services.short_description = 'Services'

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'name', 'phone', 'email')

class CompanyAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'customer', 
                    'companyname', 
                    'vat', 
                    'phone', 
                    'email', 
                    'address', 
                    'zip', 
                    'city', 
                    'country', 
                    'billing_company_name', 
                    'billing_vat', 
                    'billing_adr', 
                    'billing_zip', 
                    'billing_city', 
                    'billing_country', 
                    'billing_email')
    search_fields = ('companyname', 'vat')

class ServiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'service_name', 'is_selected')

class OrderTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'type_name')

class KeyChoiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'key_choice')

class GetKeysChoiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_keys_choice')

class GetKeysLanguageAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_keys_language')

class DeliveryRecipientAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipient')

class InvoiceRecipientAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipient')

class StatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'status')

class CountryAdmin(admin.ModelAdmin):
    list_display = ('id', 'country')



admin.site.register(Order, OrderAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(OrderType, OrderTypeAdmin)
admin.site.register(KeyChoice, KeyChoiceAdmin)
admin.site.register(GetKeysChoice, GetKeysChoiceAdmin)
admin.site.register(DeliveryRecipient, DeliveryRecipientAdmin)
admin.site.register(InvoiceRecipient, InvoiceRecipientAdmin)
admin.site.register(Status, StatusAdmin)
admin.site.register(GetKeysLanguage, GetKeysLanguageAdmin)
admin.site.register(Country, CountryAdmin)

from django.db.models.signals import post_save
from django.contrib.auth.models import User,Group
from .models import Customer



def customer_profile(sender,instance,created,**kwargs):
    if created:
        group, created = Group.objects.get_or_create(name='customer')  # This line is changed
        instance.groups.add(group)


        Customer.objects.create(
            user=instance,
            name=instance.username,
            email=instance.email,
        )
        print('profile created')

post_save.connect(customer_profile,sender=User)



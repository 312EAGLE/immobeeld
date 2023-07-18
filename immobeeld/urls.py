from django.urls import path
from projects import views
from django.contrib import admin
from django.contrib.auth import views as auth_view



urlpatterns = [
    path('', views.home, name='index.html'),
    
    path('foto', views.foto, name='foto.html'),
    path('video', views.video, name='video.html'),
    path('360', views.v360, name='360.html'),
    path('contact', views.contact, name='contact.html'),

    path('sign_up', views.register, name='sign_up.html'),
    path('login/', views.user_login, name='login.html'),
    
    
    path('admin/', admin.site.urls),
    
    path('logout/', views.user_logout, name='logout.html'),
    
    
    path('dashboard/', views.dashboard, name='dashboard.html'),
    path('update-customer/', views.update_customer, name='update-customer'),
    path('update-company/', views.update_company, name='update-company'),

    path('orders/', views.orders, name='orders.html'),
    path('createorder', views.createOrder, name='createorder.html'),
    path('ajax/company-info/<int:company_id>/', views.get_company_info, name='company-info'),
    path('download_orders/', views.download_orders, name='download_orders'),
    
    
    
]


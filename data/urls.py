from django.urls import path
from . import views

urlpatterns = [
    path('login/',views.login_page,name='login'),
    path('register/',views.register_page,name='register'),
    path('',views.home_page,name='home'),
    path('logout/',views.logout_user,name='logout')
    
]
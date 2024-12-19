from django.contrib import admin
from django.urls import path, include
# from django.views.generic import RedirectView
from users.views import home
# from users import views
from users import views as user_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard/', user_views.dashboard_redirect, name='dashboard_redirect'),
    path('users/', include('users.urls')),
    path('', home, name='home'),
    path('services/', include('services.urls')), 
]



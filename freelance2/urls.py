from django.contrib import admin
from django.urls import path, include
# from django.views.generic import RedirectView
from users.views import home
# from users import views
from users import views as user_views
from django.conf.urls import handler403


urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard/', user_views.dashboard_redirect, name='dashboard_redirect'),
    path('users/', include('users.urls',  namespace='users')),
    path('', home, name='home'),
    path('services/', include('services.urls')), 
]

handler403 = 'users.views.custom_permission_denied_view'


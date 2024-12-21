from django.urls import reverse
from .decorators import freelancer_required, client_required

# Constants for role management
ROLE_FREELANCER = 'Freelancer'
ROLE_CLIENT = 'Client'

def dashboard_url(request):
    if request.user.is_authenticated:
        if request.user.role == ROLE_FREELANCER:
            return {'dashboard_url': reverse('users:freelancer_dashboard')}
        elif request.user.role == ROLE_CLIENT:
            return {'dashboard_url': reverse('users:client_dashboard')}
    return {'dashboard_url': None}
  
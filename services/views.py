from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Service
from .forms import ServiceForm

# Create a service
@login_required
def service_create(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            service = form.save(commit=False)
            service.owner = request.user  # Assign the logged-in user as the owner
            service.save()
            return redirect('service_list')
    else:
        form = ServiceForm()
    return render(request, 'services/service_form.html', {'form': form})

# Read (list) services
def service_list(request):
    services = Service.objects.all()
    return render(request, 'services/service_list.html', {'services': services})

# Update a service
@login_required
def service_update(request, pk):
    service = get_object_or_404(Service, pk=pk, owner=request.user)  # Ensure the logged-in user is the owner
    if request.method == 'POST':
        form = ServiceForm(request.POST, instance=service)
        if form.is_valid():
            form.save()
            return redirect('service_list')
    else:
        form = ServiceForm(instance=service)
    return render(request, 'services/service_form.html', {'form': form})

# Delete a service
@login_required
def service_delete(request, pk):
    service = get_object_or_404(Service, pk=pk, owner=request.user)  # Ensure the logged-in user is the owner
    if request.method == 'POST':
        service.delete()
        return redirect('service_list')
    return render(request, 'services/service_confirm_delete.html', {'service': service})


''' 
render: Renders a template with a context.

get_object_or_404: Retrieves an object from the database or returns a 404 error if not found.

redirect: Redirects to a different URL.

login_required: Ensures that the view can only be accessed by authenticated users.

Service: The model representing the service entity.

ServiceForm: The form used to create and update services.
This view handles the creation of a new service.

Only authenticated users can access it (@login_required).

If the request method is POST, it processes the submitted form.

If the form is valid, it assigns the logged-in user as the owner of the service and saves it.

Redirects to the service_list view after saving.

If the request method is not POST, it displays an empty form.
This view lists all the services.

It retrieves all service objects from the database and renders them in the service_list.html template.
This view handles updating an existing service.

Only the owner of the service can update it (get_object_or_404 ensures the logged-in user is the owner).

If the request method is POST, it processes the submitted form with the instance of the existing service.

If the form is valid, it saves the changes and redirects to the service_list view.

If the request method is not POST, it displays the form pre-filled with the service's data.
This view handles deleting a service.

Only the owner of the service can delete it (get_object_or_404 ensures the logged-in user is the owner).

If the request method is POST, it deletes the service and redirects to the service_list view.

If the request method is not POST, it displays a confirmation page.

In summary, these views provide a complete CRUD (Create, Read, Update, Delete) interface for managing services in a Django application. 
Each view ensures that only authenticated users can create, update, or delete services and that only the owner of a service can update or delete it.
'''
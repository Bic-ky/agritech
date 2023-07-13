
from django.contrib.admin.sites import site
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from account.forms import UserProfileForm
from account.models import User, UserProfile
from account import admin
import ecom
from ecom.admin import ProjectAdmin
from ecom.models import ExtraImage, ProjectStatus
from .models import Vendor
from .forms import ProjectStatusForm, VendorForm
from django.http import JsonResponse
from django.contrib import messages

from django.forms.models import inlineformset_factory


from account.views import check_role_vendor
from ecom.models import Category, Project
from ecom.forms import EditProjectForm, ProjectForm 

from ecom.models import ProjectStatus,Category, Project
from account.views import check_role_vendor
from ecom.forms import ProjectForm

from django.template.defaultfilters import slugify
from orders.models import Order, FarmOrder
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db.models import Count,Sum
# Create your views here.




@login_required(login_url='account:login')
@user_passes_test(check_role_vendor)
def vprofile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    vendor = get_object_or_404(Vendor, user=request.user)

    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        vendor_form = VendorForm(request.POST, request.FILES, instance=vendor)

        if profile_form.is_valid() and vendor_form.is_valid():
            profile_form.save()
            vendor_form.save()
            messages.success(request, 'Settings updated.')
            return redirect('account:vprofile')
        else:
            messages.error(request, 'Error occurred while saving the form.')
    else:
        profile_form = UserProfileForm(instance=profile)
        vendor_form = VendorForm(instance=vendor)

    context = {
        'profile_form': profile_form,
        'vendor_form': vendor_form,
        'profile': profile,
        'vendor': vendor,
    }
    return render(request, 'vendor/vprofile.html', context)



def get_vendor(request):
    vendor = Vendor.objects.get(user=request.user)
    return vendor


from django.db.models import Count, Q
@login_required(login_url='account:login')
@user_passes_test(check_role_vendor)
def menu_builder(request):
    vendor = get_vendor(request)
    categories = Category.objects.annotate(num_projects=Count('project', filter=Q(project__vendor=vendor.user))).order_by('created_at')
    context = {
        'categories': categories,
    }
    return render(request, 'vendor/menu_builder.html', context)



@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def productItem_by_category(request, pk=None):
    category = get_object_or_404(Category, pk=pk)
    vendor = get_object_or_404(Vendor, user=request.user)

    productItem = Project.objects.filter(project_type=category, vendor=vendor.user)
    context = {
        'productItem': productItem,
        'category': category,
        'vendor': vendor,
    }
    return render(request, 'vendor/productItem_by_category.html', context)

@login_required(login_url='account:login')
@user_passes_test(check_role_vendor)
def add_product(request):
    vendor = get_vendor(request)
    if not vendor.is_approved:
        messages.error(request, 'You are not approved to add products. Please add your details for approval.')
        return redirect('account:vprofile')

    form = ProjectForm()
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.vendor = request.user
            product.slug = slugify(product.project_title)
            
            # Calculate and assign total number of shares available
            value_of_share = product.value_of_share
            demand = product.total_cost - product.fund_invested
            num_shares = round(demand / value_of_share)
            product.total_no_shares = num_shares
            
            product.save()

            # Process extra images
            extra_images = request.FILES.getlist('extra_images')
            for extra_image in extra_images:
                extra_image_instance = ExtraImage(project=product, image=extra_image)
                extra_image_instance.save()

            messages.success(request, 'Product added successfully!')
            return redirect('account:productItem_by_category', product.project_type.id)
        else:
            messages.error(request, 'Error adding product. Please correct the form errors.')
            print(form.errors)
    


    context = {
        'form': form,
        # Get the HTML representation of the map
    }

    # Create an instance of ProjectAdmin
    model_admin = ecom.admin.ProjectAdmin(Project, site)

  
    
    return render(request, 'vendor/add_product.html', context)

@login_required(login_url='account:login')
@user_passes_test(check_role_vendor)
def edit_product(request, pk=None):
    product = get_object_or_404(Project, pk=pk)

    if request.method == 'POST':
        form = EditProjectForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()

            # Process extra images
            extra_images = request.FILES.getlist('extra_images')
            # product.extra_images.all().delete()  # Remove existing extra images
            for extra_image in extra_images:
                extra_image_instance = ExtraImage(project=product, image=extra_image)
                extra_image_instance.save()

            messages.success(request, 'Product updated successfully!')
            return redirect('account:productItem_by_category', product.project_type.id)
        else:
            messages.error(request, 'Error updating product. Please correct the form errors.')
            print(form.errors)
    else:
        form = EditProjectForm(instance=product)

    context = {
        'form': form,
        'product': product,
    }
    return render(request, 'vendor/edit_product.html', context)



# @login_required(login_url='account:login')
# @user_passes_test(check_role_vendor)
# def delete_product(request, pk=None):
#     product = get_object_or_404(Project, pk=pk)
#     product.delete()
#     messages.success(request, 'Product has been deleted successfully!')
#     return redirect('account:productItem_by_category', product.project_type.id)


def order_detail(request, order_number):
    try:
        vendor = get_vendor(request)
        order = Order.objects.filter(order_number=order_number, is_ordered=True, vendors__user=vendor.user).first()
        ordered_product = FarmOrder.objects.filter(order=order, project__vendor=vendor.user)

        context = {
            'order': order,
            'ordered_product': ordered_product,
            'subtotal': order.total - order.total_tax,
            'tax_data': order.get_total_by_vendor(vendor)['tax_dict'],
            'grand_total': order.get_total_by_vendor(vendor)['grand_total'],
        }
        
        return render(request, 'vendor/order_detail.html', context)
    
    except Order.DoesNotExist:
        return redirect('account:vendor')




def my_orders(request):
    vendor = Vendor.objects.get(user=request.user)
    orders = Order.objects.filter(vendors__in=[vendor.id], is_ordered=True).order_by('-created_at')

    context = {
        'orders': orders,
    }
    return render(request, 'vendor/my_orders.html', context)







@login_required(login_url='account:login')
def active_farms(request):
    user = request.user
    active_projects = user.project_set.filter(is_approved=True, is_available=True)

    # Search functionality
    search_query = request.GET.get('search', '')  # the search query from the GET parameters
    if search_query:
        active_projects = active_projects.filter(project_title__icontains=search_query)

    if request.method == 'POST':
        form = ProjectStatusForm(request.POST)
        if form.is_valid():
            project_id = request.POST.get('project_id')  # the project ID from the POST data
            form.instance.project_id = project_id  # Assign the project ID to the form instance
            form.save()
            message = 'Status update successful'
            messages.success(request, message)  # Add success message
            return JsonResponse({'message': message})
        else:
            return JsonResponse({'error': form.errors})
    else:
        form = ProjectStatusForm()

    context = {'active_projects': active_projects, 'form': form, 'search_query': search_query}
    return render(request, 'vendor/active_farms.html', context)



@login_required(login_url='account:login')
def completed_farms(request):
    user = request.user
    completed_projects = user.project_set.filter(is_approved=True, is_completed=True)

    # Search functionality
    search_query = request.GET.get('search', '')  # the search query from the GET parameters
    if search_query:
        completed_projects = completed_projects.filter(project_title__icontains=search_query)

    context = {'completed_projects': completed_projects,  
               'search_query': search_query}
    return render(request, 'vendor/completed_farms.html', context)


def save_status(request, project_id):
    print(project_id)  # Print the project_id variable
    if request.method == 'POST':
        form = ProjectStatusForm(request.POST)
        if form.is_valid():
            form.instance.project_id = project_id  # Assign the project ID to the form instance
            form.save()  # Save the form data in the model
            
        else:
            print(form.errors)  # Print form errors to the console for debugging
            return JsonResponse({'error': 'Form data is invalid'})



from django.db.models import F
from ecom.models import ProjectStatus

@login_required(login_url='account:login')
def farm_status(request, id):
    orders = Order.objects.filter(user=request.user, is_ordered=True)
    project = get_object_or_404(Project, id=id)
    progress_ratio = (project.collected_amount / project.demand) * 100
    
    # status messages for the specific project ID
    status_messages = ProjectStatus.objects.filter(project_id=id).order_by('created_at')
    
    # the users who have ordered the specific farm
    ordered_users = User.objects.filter(farmorder__project=project).distinct()
    

        # Retrieve the FarmOrder data for the specific project and calculate the sum of quantity and return_amount for each user
    invested_projects = FarmOrder.objects.filter(project=project).values('user').annotate(
        total_quantity=Sum('quantity'),
        total_return_amount=Sum('return_amount'),
        invested_amount = Sum('amount')
    )

    combined_farm_orders = []
    for user in ordered_users:
        quantity_sum = FarmOrder.objects.filter(user=user, project=project).aggregate(Sum('quantity'))['quantity__sum'] or 0
        invested_projects = FarmOrder.objects.filter(project=project).values('user').annotate(total_quantity=Sum('quantity'),
        total_return_amount=Sum('return_amount'),invested_amount = Sum('amount'))
        combined_farm_orders.append({'user': user, 'quantity': quantity_sum , 'invested_projects':invested_projects})
        
    quantity = combined_farm_orders[0]['quantity'] if combined_farm_orders else 0

   

    context = {
        'project': [project],
        'progress_ratio': progress_ratio,
        'status_messages': status_messages,
        'farm_orders': combined_farm_orders,
        'combined_farm_orders': quantity,
        'invested_projects' : invested_projects
    }
    
    return render(request, 'vendor/farm_status.html', context)







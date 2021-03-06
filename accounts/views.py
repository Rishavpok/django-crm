from multiprocessing import context
from unicodedata import name
from django.shortcuts import render , redirect
from django.http import HttpResponse
from accounts.models import *
from .forms import OrderForm,createUserForm
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login , logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.




def registerPage(request):
    form = createUserForm()

    if request.method == 'POST':
        form = createUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for' ,+ user )
            return redirect('login')
    context = {'form': form}
    return render(request, 'accounts/register.html', context)



def loginPage(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username or Password doesnot match')
    return render(request, 'accounts/login.html')

def logoutuser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()
    # total_customers = customer.count()
    total_order = orders.count()
    delivered = orders.filter(status='Delivired').count()
    pending = orders.filter(status='Pending').count()
    context = {'orders': orders,
               'customers': customers,
               'total_order': total_order,
               'delivered': delivered,
               'pending': pending}
    return render(request, 'accounts/dashboard.html', context)

@login_required(login_url='login')
def product_data(request):
    products = Product.objects.all()

    return render(request, 'accounts/products.html', {'products': products})

@login_required(login_url='login')
def customer(request, pk_test):
    customer = Customer.objects.get(id=pk_test)
    orders = customer.order_set.all()
    order_count = orders.count()
    context = {'customer': customer, 'orders': orders, 'order_count': order_count}

    return render(request, 'accounts/customer.html', context)

@login_required(login_url='login')
def create_order(request,pk):
    OrderFormSet = inlineformset_factory(Customer, Order ,  fields=('product', 'status'))
    customer = Customer.objects.get(id=pk) 
    formset = OrderFormSet(instance=customer)
    # form = OrderForm(initial={'customer': customer})
    if request.method == 'POST':
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')
    context= {'formset': formset}
    return render(request, 'accounts/order_form.html' , context )


@login_required(login_url='login')
def update_order(request , pk):

    order = Order.objects.get(id=pk)

    form = OrderForm(instance=order)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')
    context={'form':form}
    return render(request, 'accounts/order_form.html', context)

@login_required(login_url='login')
def delete_order(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('/')
    context ={'item': order}
    return render(request, 'accounts/delete.html', context)
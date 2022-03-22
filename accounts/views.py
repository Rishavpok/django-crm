from django.shortcuts import render , redirect
from django.http import HttpResponse
from accounts.models import *
from .forms import OrderForm
from django.forms import inlineformset_factory
# Create your views here.


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


def product_data(request):
    products = Product.objects.all()

    return render(request, 'accounts/products.html', {'products': products})


def customer(request, pk_test):
    customer = Customer.objects.get(id=pk_test)
    orders = customer.order_set.all()
    order_count = orders.count()
    context = {'customer': customer, 'orders': orders, 'order_count': order_count}

    return render(request, 'accounts/customer.html', context)


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


def delete_order(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('/')
    context ={'item': order}
    return render(request, 'accounts/delete.html', context)
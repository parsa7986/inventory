from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from urllib import request
from django.views import View 
from .models import Products , Customer , Cart , Payment , OrderPlaced , Warehouse
from django.views.generic import TemplateView
from .forms import CustomerRegistrationForm , CustomerProfileForm , WarehouseForm
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import user_passes_test
# Create your views here.
class HomeView(TemplateView):
    template_name = "app/home.html"

class AboutView(TemplateView):
    template_name = "app/about.html"

class ContactView(TemplateView):
    template_name = "app/contact.html"        

class Category(View):
    def get(self,request,val):
        product = Products.objects.filter(category=val)
        title = Products.objects.filter(category=val).values('title')
        return render(request,"app/category.html",locals())
    
class ProductDetail(View):
    def get(self,request,pk):
        product= Products.objects.get(pk=pk)
        return render(request,"app/productdetail.html",locals())
            

class CategoryTitle(View):
    def get(self,request,val):
        product=Products.objects.filter(title=val)
        title=Products.objects.filter(category=product[0].category).values('title')
        return render(request,"app/category.html",locals())

class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, "app/customeregistration.html", {'form': form})

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Congrats! You have registered successfully!")
        else:
            messages.warning(request, "Input not valid!")

        return render(request, "app/customeregistration.html", {'form': form})

class ProfileView(View):
    def get(self,request):
        form = CustomerProfileForm()
        return render(request,"app/profile.html",locals())
    def post(self,request):
        form = CustomerProfileForm()
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            mobile = form.cleaned_data['mobile']
            reg = Customer(user=user, name=name, locality=locality, mobile=mobile, city=city)
            reg.save()
            messages.success(request,"Congrats")
        else:
            messages.warning(request,"invalid input")    

        return render(request,"app/profile.html",locals())

def add_to_cart(request):
    user = request.user

    if request.method == 'GET':
        product_id = request.GET.get('prod_id')
    elif request.method == 'POST':
        product_id = request.POST.get('prod_id')
    else:
        # Handle the case when the request method is not supported
        return HttpResponse("Invalid request method")

    if product_id:
        try:
            product = Products.objects.get(id=product_id)
            Cart(user=user, product=product).save()
            return redirect("/cart")
        except Products.DoesNotExist:
            # Handle the case when the product with the given ID doesn't exist
            return HttpResponse("Invalid product ID")
    else:
        # Handle the case when no product_id is provided
        return HttpResponse("No product ID provided Please enter your product id manually in url bar that is 1 for first grade pistachio,2 for first grade Almonds,3 for first grade hazelnut, 4 for first grade walnut,5 for first grade dates and in this order for second grade")


def show_cart(request):
    amount=0
    user=request.user
    cart=Cart.objects.filter(user=user)
    for p in cart:
        value= p.quantity * p.product.selling_price
        amount = amount+value
    totalamount= amount +40     
    return render(request,"app/addtocart.html",locals())

def plus_cart(request):
    if request.method == 'GET':
        prod_id=request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id)& Q(user=request.user))
        c.quantity+=1
        c.save()
        user=request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value= p.quantity * p.product.selling_price
            amount = amount+value
        totalamount= amount +40 

        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount,
        }
        return JsonResponse(data)
    
def remove_cart(request):
         if request.method == 'GET':
            prod_id=request.GET['prod_id']
            c = Cart.objects.get(Q(product=prod_id)& Q(user=request.user))
            c.delete()
            user=request.user
            cart = Cart.objects.filter(user=user)
            amount = 0
            for p in cart:
                value= p.quantity * p.product.selling_price
                amount = amount+value
            totalamount= amount +40 

            data={
                'quantity':c.quantity,
                'amount':amount,
                'totalamount':totalamount,
        }
            return JsonResponse(data)
         
class Checkout(View):
    def get(self,request):
        user=request.user
        add = Customer.objects.filter(user=user)
        cart_items=Cart.objects.filter(user=user)
        famount=0
        for p in cart_items:
            value = p.quantity * p.product.selling_price
            famount= famount + value
        totalamount= famount+40    
        return render(request,"app/checkout.html",locals())         
    

def show_orders(request):
    # Retrieve all order records from the database
    orders = OrderPlaced.objects.all()

    # Pass the order records to the template
    return render(request, 'app/status.html', {'orders': orders})

def warehouse_list(request):
    warehouses = Warehouse.objects.all()
    return render(request, 'app/warehouse_list.html', {'warehouses': warehouses})

def warehouse_detail(request, warehouse_id):
    warehouse = get_object_or_404(Warehouse, id=warehouse_id)
    return render(request, 'app/warehouse_detail.html', {'warehouse': warehouse})

def is_superuser(user):
    return user.is_superuser

@user_passes_test(is_superuser)
def warehouse_create(request):
    if request.method == 'POST':
        form = WarehouseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('warehouse_list')
    else:
        form = WarehouseForm()
    return render(request, 'app/warehouse_create.html', {'form': form})
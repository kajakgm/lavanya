import json
from django.shortcuts import render,redirect
from .models import *
from django.contrib import messages
from myapp.form import CustomUserForm
from django.contrib.auth import authenticate,login,logout
from django.http import JsonResponse
# Create your views here.
def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
        storage = messages.get_messages(request)
        storage.used = True  # Clears old messages
        messages.success(request,'Logeed out success')
        return redirect('/')
def home(request):
    products=Products.objects.filter(trending=1)
    return render (request,'shop/index.html',{'products':products})
def login_page(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:

        if request.method=="POST":
            name=request.POST.get('username')
            pwd=request.POST.get('password')
            user=authenticate(request,username=name,password=pwd)
            if user is not None:
                login(request,user)
                messages.success(request,'logged in sucess')
                return redirect("/")
            else:
                messages.error(request,'invalid user credentials')
                return redirect('/login')

        
            
        return render(request,'shop/login.html')
def register(request):
    form=CustomUserForm()
    if request.method=="POST":
        form=CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Registration Success")
            return redirect('/login')
    return render(request,'shop/register.html',{'form':form})
def collections(request):
    catagory=Catagory.objects.filter(status=0)
    return render(request,'shop/collections.html',{"catagory":catagory})
def collectionsview(request,name):
    if(Catagory.objects.filter(name=name,status=0)):
        products=Products.objects.filter(category__name=name)
        return render(request,'shop/products/index.html',{"products":products,"category_name":name})
    else:
        messages.warning(request,"No such Category Found")
        return redirect('collections')
def product_details(request,cname,pname):
    if(Catagory.objects.filter(name=cname,status=0)):
        if Products.objects.filter(name=pname,status=0):
            products=Products.objects.filter(name=pname,status=0).first()
            return render(request,'shop/products/product_details.html',{'products':products})
        else:
            messages.warning(request,"No such Category Found")
            return redirect('collections')
    else:
            messages.warning(request,"No such Category Found")
            return redirect('collections')
def add_to_cart(request):
    if request.headers.get('x-requested-with')=='XMLHttpRequest':
        if request.user.is_authenticated:
            data=json.load(request)
            product_qty=data['product_qty']
            product_id=data['pid']
            print(request.user.id)
            product_status=Products.objects.get(id=product_id)
            if product_status:
                if cart.objects.filter(user=request.user,product_id=product_id):
                    return JsonResponse({'status':'product already in cart'})
                else:
                    if product_status.qty >= product_qty:
                        #cart.objects.create(user=request.user,product_id=product_id,product_qty=product_qty)
                        cart.objects.create(user=request.user, product_id=product_id, product_qty=product_qty)

                    else:
                        return JsonResponse({'status':'Stock not avaialable'})

            #return JsonResponse({'status':'product added to cart success'},status=200)
        else:
            return JsonResponse({'status':'Login to Add Cart'},status=200)
        pass
    else:
        return JsonResponse({'status':'Invalid Access'},status=200)
    
def cart_page(request):
    if request.user.is_authenticated:
        cart_items=cart.objects.filter(user=request.user)
        print(cart_items)
        #return render(request,'shop/cart.html',{"cart":cart_items})
        return render(request, 'shop/cart.html', {"cart_items": cart_items})

    else:
        return redirect('/')
def remove_cart(request,cid):
    cartitem=cart.objects.get(id=cid)
    cartitem.delete()
    return redirect('/cart')
def fav_page(request):
    pass
    if request.headers.get('x-requested-with')=='XMLHttpRequest':
        if request.user.is_authenticated:
            data=json.load(request)
            
            product_id=data['pid']
            print(request.user.id)
            product_status=Products.objects.get(id=product_id)
            if Favourite.objects.filter(user=request.user.id,product_id=product_id):
                return JsonResponse({'status':'already in favourite'},status=200)
            else:
                Favourite.objects.create(user=request.user, product_id=product_id,)
                return JsonResponse({'status':'Product added to favourite'},status=200)
            
            
        else:
            return JsonResponse({'status':'Login to Add Cart'},status=200)
        pass
    else:
        return JsonResponse({'status':'Invalid Access'},status=200)
def favviewpage(request):
    if request.user.is_authenticated:
        fav=Favourite.objects.filter(user=request.user)
        
        #return render(request,'shop/cart.html',{"cart":cart_items})
        return render(request, 'shop/fav.html', {"fav": fav})

    else:
        return redirect('/')
def remove_fav(request,fid):
    favitem=Favourite.objects.get(id=fid)
    favitem.delete()
    return redirect('/favviewpage')
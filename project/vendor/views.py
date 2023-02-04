from django.shortcuts import render,redirect
from django.contrib import messages 
from django.contrib.auth import authenticate,login,logout
from django.db import models
from user.models import myuser,Userdetail
from product.models import Vehicles
from categories.models import Category
from user.otp import check_otp,sentOTP
from django.views.decorators.cache import cache_control
from product.forms import Vehicleforms
from orders.models import OrderVehicle,Orders
from django.views.decorators.cache import never_cache
#from django.contrib.auth.decorators import login_required

# Create your views here.


@cache_control(no_cache = True,must_revalidate = True,no_store = True)
def vendor_register(request):
    if 'vendor' in request.session:
        return redirect ('vendor:vendor_dashboard')

    if request.method == 'POST':
        first_name = request.POST['username']
        GST_NUMBER = request.POST['GST_NUMBER']
        email = request.POST['email']
        mobile = request.POST['mobile']
        password = request.POST['password']

        if first_name == '':
            messages.info(request,'name is empty')
            return redirect(vendor_register)
        elif email == '':
                messages.info(request,'Email is empty')
                return redirect(vendor_register)
        elif password == '':
                messages.info(request,'password is empty')
                return redirect(vendor_register)
       # elif myuser.objects.filter(mobile=mobile):
                #messages.info(request,'Mobile alread exists')
        else:
                request.session['first_name'] = first_name
                request.session['GST_NUMBER'] = GST_NUMBER
                request.session['email'] = email
                request.session['mobile'] = mobile
                request.session['password'] = password
                sentOTP(mobile)
                return redirect('vendor:verify_vender')
    return render(request,'vendor_temp/vendor_register.html')


@cache_control(no_cache = True,must_revalidate = True,no_store = True)
def verify_vender(request):
    # if 'vendor' in request.session:
    #     return redirect ('vendor:vendor_dashboard')
    if request.method == 'POST':
        get_otp = request.POST.get('otp')
        phone_number =  request.session['mobile'] 
        
        if check_otp(phone_number,get_otp):
            first_name =   request.session['first_name'] 
            GST_NUMBER =    request.session['GST_NUMBER'] 
            email =    request.session['email'] 
            mobile =    request.session['mobile'] 
            password =    request.session['password'] 
            del request.session['email']
            del request.session['first_name']
            del request.session['GST_NUMBER']
            del request.session['mobile'] 
            del request.session['password']
            
            user = myuser.objects.create_vendor(first_name=first_name,gst_no=GST_NUMBER,mobile=mobile,email=email,password=password)
            user.save()
            #vendor = myuser.objects.create_vendor(email=email,password=password,mobile=mobile)
            #vendor.save()
            return redirect('vendor:vendor_signin')
        else:
            messages.info(request,'invalid otp number')
    return render(request,'register_otp.html')

@cache_control(no_cache = True,must_revalidate = False,no_store = True)
def vendor_signin(request):
    if 'vendor' in request.session:
        return redirect ('vendor:vendor_dashboard')
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        if email == '':
            messages.info(request,'email is empty')
            return redirect(vendor_signin)
        elif password == '':
                messages.info(request,'password is empty')
                return redirect(vendor_signin)
        else:
            vendor = authenticate(email=email,password=password)
            if vendor is not None:
                if vendor.is_staff == True:
                    if vendor.is_active == True:
                          request.session['vendor']=email
                          login(request,vendor)
                          return redirect('vendor:vendor_dashboard')
                    else:
                         messages.info(request,'you are blocked by admin')
                else:
                    messages.info(request,'you are not a vendor')
                    
            else:
                messages.info(request,'You are blocked by admin')
            return redirect('vendor:vendor_signin')
    return render (request,'vendor_temp/vendor_signin.html')


def vendor_logout(request):
         if 'vendor'  in request.session:
              del request.session['vendor']
              logout(request)
              return redirect('vendor:vendor_signin')


@cache_control(no_cache = True,must_revalidate = False,no_store = True)
def vendor_dashboard(request):
    if 'vendor' in request.session:
       
        return redirect('vendor:vendor_profile')

        
    else:
        messages.info(request,"please login")
        return redirect ('vendor:vendor_signin')

def vendor_profile(request):
    try:

        email =  request.user.email
        user = request.user
        detail = myuser.objects.get(email = email)
        # detail = myuser.objects.get(user_id  = user)

        context = {
            'detail':detail,
            }
        return render(request,'vendor_temp/panel.html',context)
    except:
        return render(request,'vendor_temp/panel.html')

    



#====================================product mgmt=================================

@cache_control(no_cache = True,must_revalidate = False,no_store = True)
def view_vehicles(request):
    if 'vendor' in request.session:
        
        try:

            vendor = myuser.objects.get(email=request.user.email)
            vehicle = Vehicles.objects.filter(vendor_id = vendor.id ,is_available =True)
            return render(request,'vendor_temp/view_vehicles.html',{'vehicle':vehicle})
        except:
            return redirect('vendor:vendor_signin')
        
@cache_control(no_cache = True,must_revalidate = False,no_store = True)
def Non_Available_vehicles(request):
    if 'vendor' in request.session:
        
        try:

            vendor = myuser.objects.get(email=request.user.email)
            vehicle = Vehicles.objects.filter(vendor_id = vendor.id ,is_available =False)
            return render(request,'vendor_temp/non_avilable_vehicle.html',{'vehicle':vehicle})
        except:
            return redirect('vendor:vendor_signin')

@cache_control(no_cache = True,must_revalidate = False,no_store = True)
def add_vehicles(request):
    if 'vendor' in request.session:
        form = Vehicleforms()
       
        if request.method == 'POST':
            email = request.user.email
            vendor = myuser.objects.get(email =email)
            form = Vehicleforms(request.POST, request.FILES)
            if form.is_valid():   
                form.instance.vendor_id = vendor        
                form.save()
                messages.success(request, ('Vehicle Added!'))
            else:
                 messages.success(request, ('Data is not valid!'))
                 
		   



            # vehicle_name = request.POST['vehicle_name']
            # category = request.POST['category']
            # Range = request.POST['range']
            # speed = request.POST['speed']
            # slug = request.POST['slug']
            # image = request.FILES['image']
            # email = request.user.email
            # vendor = myuser.objects.get(email =email)

            # vehicle =Vehicles.objects.create(vendor_id = vendor,vehicle_name=vehicle_name,category=Category.objects.get(category_name=category,),
            # range=Range,top_speed= speed,image=image,slug=slug)
            # vehicle.save()
            return redirect('vendor:view_vehicles')
    return render(request,'vendor_temp/add_vehicles.html',{'form':form})



def delete_vehicle(request,pk):
    
    vehicle= Vehicles.objects.get(id=pk)
    vehicle.delete()
    return redirect('vendor:view_vehicles')

@cache_control(no_cache = True,must_revalidate = False,no_store = True)
def edit_vehicle(request,pk):
    vehicle = Vehicles.objects.get(id=pk)
    if request.method == 'POST':
        vehicle_name = request.POST['vehicle_name']
        category = request.POST['category']
        range = request.POST['range']
        speed = request.POST['speed']
        slug = request.POST['slug']
        image = request.FILES['image']
        
        #try:
        vehicle.vehicle_name =vehicle_name
        vehicle.category =Category.objects.get(category_name=category)
        vehicle.range =range
        vehicle.top_speed=speed
        vehicle.slug=slug
        vehicle.image=image
        vehicle.save()
        return redirect('vendor:view_vehicles')
        #except:
            #messages.info(request,'Not a valid data please check')

    return render(request,'vendor_temp/update_vehicle.html',{'vehicle':vehicle})

@cache_control(no_cache = True,must_revalidate = False,no_store = True)
def active_vehicle(request,pk):
    vehicle = Vehicles.objects.get(id=pk)
    vehicle.is_available = True
    vehicle.save()
    return redirect('vendor:Non_Available_vehicles')
@cache_control(no_cache = True,must_revalidate = False,no_store = True)
def deactive_vehicle(request,pk):
    vehicle = Vehicles.objects.get(id=pk)
    vehicle.is_available = False
    vehicle.save()
    return redirect('vendor:view_vehicles')


#==============================ORDERS==============================#

@cache_control(no_cache = True,must_revalidate = False,no_store = True)
def Orders(request):
    if 'vendor' in request.session:
         vendor = myuser.objects.get(email=request.user.email)
     
    # vehicle = Vehicles.objects.filter(vendor_id = vendor.id )
         orderd_vehicle =OrderVehicle.objects.filter(vehicles_id__vendor_id =vendor.id)
         context = { 
          'orderd_vehicle':orderd_vehicle
           }
         return render (request,'vendor_temp/Orders.html',context)

@cache_control(no_cache = True,must_revalidate = False,no_store = True)
def cancel_order(request,pk):
    if 'vendor' in request.session:
         orders= OrderVehicle.objects.get(id = pk)
         orders.status = 'Cancelled'
         orders.save()
         return redirect('vendor:Orders')
@cache_control(no_cache = True,must_revalidate = False,no_store = True)
def order_details(request,pk):
    if 'vendor' in request.session:
         order = OrderVehicle.objects.get(id =pk)
         print(order)
         context = {
          'order':order 
           }
         return render(request,'vendor_temp/Orders_detail.html',context)








# def add_varient(request,pk):
#     if request.method == 'POST':
#         vehicle = Vehicles.objects.get(id=pk)
#         price =request.POST['price']
#         image1 = request.FILES['image1']
#         image2  = request.FILES['image2']
#         image3 = request.FILES['image3']
#         color =request.POST['color']
       
#         remaining = request.POST['remaining']


#         variant = Variant.objects.create(vehicle_id = vehicle,image1=image1,image2=image2,image3=image3,price=price,remaining=remaining,color_name=color)
#         variant.save()
#         return redirect('view_vehicles')


#     return render(request,'vendor_temp/add_variant.html')

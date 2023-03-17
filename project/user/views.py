from django.shortcuts import render,redirect
from . models import myuser,Userdetail
from django.contrib import messages,auth 
from django.contrib.auth import authenticate
#import random
from user.otp import check_otp,sentOTP
#from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from product.models import Vehicles,Variant,Review
from categories.models import Category
from Cartapp.models import CartItem
from adminapp.models import Banner
from.models import myuser,Userdetail
from orders.models import Orders,OrderVehicle
from .forms import editprofile
from django.views.decorators.cache import never_cache
from product.forms import Reviewforms
from user.models import Userdetail

from.helpers import send_forget_password_mail
import uuid
from django.http import JsonResponse

# Create your views here.

@never_cache
def home(request):
       if 'username' in request.session:
            category = Category.objects.all()
          #  image = Category.objects.filter(category_name = 'SPORTS')
            vehicles = Vehicles.objects.filter(is_available=True)[:6]
            banner = Banner.objects.filter(status ='Active')
            context ={
           'category':category,
            'vehicles':vehicles,
            'banner':banner,
            
             }
       else:
            category = Category.objects.all()[:6]
            vehicles = Vehicles.objects.filter(is_available=True)[:9]
            banner = Banner.objects.filter(status ='Active')
           
            context ={
                 'category':category,
                 'vehicles':vehicles,
                 'banner':banner,
             }
       
       
       return render(request,'user_temp/home.html',context)




@never_cache
def user_register(request):
    if 'username' in request.session:
        return redirect('user:home')
    
    if request.method == 'POST':
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email']
            mobile = request.POST['mobile']
            password = request.POST['password']
           


            if first_name == '':
               
                messages.info(request,'username is empty')
            elif first_name.strip() == '':
                messages.info(request,'username first letter should be capital')
            elif first_name != first_name.capitalize():
                messages.info(request,'username first letter should be capital')
               
            elif email == '':
                messages.info(request,'Email is empty')
                
            elif password == '':
                messages.info(request,'password is empty')
                
            elif myuser.objects.filter(email=email):
                messages.info(request,'Email is already taken')
                
            #elif myuser.objects.filter(mobile=mobile):
               # messages.info(request,'Mobile alread exists')
            else:
                request.session['first_name'] = first_name
                request.session['last_name'] = last_name
                request.session['email'] = email
                request.session['mobile'] = mobile
                request.session['password'] = password

                sentOTP(mobile)
                #Rotp = random.randint(1000,9999)
                #message_handler = MessaHandler(mobile,Rotp).send_otp_on_mobile()
                return redirect('user:verify_otp')
            return redirect('user:user_register')
            
    return render(request,'user_temp/user_signup.html')

@never_cache
def verify_otp(request):
    if 'username' in request.session:
        return redirect('user:home')

    if request.method =='POST':
        get_otp = request.POST.get('otp')
        phone_number =  request.session['mobile'] 
        
        if check_otp(phone_number,get_otp):

            first_name =   request.session['first_name'] 
            Last_name =    request.session['last_name'] 
            email =    request.session['email'] 
            mobile =    request.session['mobile'] 
            password =    request.session['password'] 

            del request.session['email']
            del request.session['first_name']
            del request.session['last_name']
            del request.session['mobile'] 

            del request.session['password']

            user = myuser.objects.create_user(first_name=first_name,last_name=Last_name,mobile=mobile,email=email,password=password)
            user.save()

            # id = myuser.objects.get(id = user.id)
            
            # cart = Cart.objects.create(
            #          user_id = id,
            #          total = 0
            #     )  
            # cart.save()
            # request.session['cart_id'] = str(cart)

            # print(request.session.get('cart_id'))

            return redirect('user:user_signin')
        else:
            messages.info(request,'invalid otp number')
            del request.session['email']
            del request.session['first_name']
            del request.session['last_name']
            del request.session['mobile'] 

    return render(request,'register_otp.html')



@never_cache
def user_signin(request):
    if 'username' in request.session:
        return redirect('user:home')
   
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        try:
            user = authenticate(email = email,password = password)

        except:
            user = None
            pass
        if user is not None and user.is_active == True and user.is_staff == False:
            auth.login(request,user)
            request.session['username']= email
           

            # cart = Cart.objects.get(user_id =user.id)
            # request.session['cart_id'] = str(cart)
            # print(request.session.get('cart_id'))
            return redirect('user:home')
        else:
            messages.warning(request,'invalid credintial')
            return redirect('user:user_signin')

    return render (request,'user_temp/user_signin.html')
    #return render(request,'register_otp.html')

def logout_user(request):
    if 'username' in request.session:
       del request.session['username']
       auth.logout(request)
       return redirect('user:home')
    return redirect('user:home')
    
    
def single_products(request,pk):

    vehicle = Vehicles.objects.get(id=pk)
    featured = Vehicles.objects.filter(is_available=True)
    category = Category.objects.get(category_name=vehicle.category)
    all_variants = Variant.objects.filter(vehicle_id =pk)
    variants = Variant.objects.filter(vehicle_id =pk)[0:3]
    try:
        review_first = Review.objects.filter(product=pk).order_by('id').last()
        review = Review.objects.filter(product = pk).order_by('id').exclude(id = review_first.id)
    except :
       review = None
    

    
   
    #cart_itemscount  = CartItem.objects.filter(user = request.user, is_active = True).count()
    #variant = Variant.objects.get(vehicle_id=pk)
    context = {
        'vehicle': vehicle,
        'category': category,
        'featured':featured,
        'variants': variants,
        'all_variants':all_variants,
        'review':review,
        'review_first':review_first,
        
        #'variant':variant,
    }
    return render(request,'user_temp/single_products.html',context)


def variant_detail(request,pk):
    varient = Variant.objects.get(id=pk)
    all_varient = Variant.objects.filter(vehicle_id = varient.vehicle_id.id)
    print(all_varient)
    context = {
       'varient':varient ,
       'all_varient': all_varient
    }
    return render(request,'user_temp/variants_detail_page.html',context)



def Shop(request):
    vehicles = Vehicles.objects.filter(is_available=True)
    category= Category.objects.all
    context = {
        'vehicles':vehicles,
        'category':category
        # 'cart_itemscount':cart_itemscount
    }
    return render(request,'user_temp/shop.html',context)



def search(request):
    if request.method == 'GET':
        search = request.GET.get('query')
        vehicles = Vehicles.objects.all().filter(vehicle_name__icontains=search,is_available=True)
        category= Category.objects.all
    context = {
        'vehicles':vehicles,
        'category':category,
        # 'cart_itemscount':cart_itemscount
    }
    return render(request,'user_temp/shop.html',context)


def auto_search_ajax(request):
    #vehicles = Vehicles.objects.all
    vehicles = Vehicles.objects.filter(is_available=True).values_list('vehicle_name',flat=True,)
    vehicle_list = list(vehicles)
    print(vehicle_list)
    return JsonResponse(vehicle_list,safe=False)




def category_filter(request,id):
     vehicles = Vehicles.objects.filter(category=id,is_available=True)
     category= Category.objects.all
     context = {
        'vehicles':vehicles,
        'category':category,
        # 'cart_itemscount':cart_itemscount
    }
     return render(request,'user_temp/shop.html',context)
    
    

#=======================================user Profile=================================================================
# class user_profile(TemplateView):
#     template_name ='user_temp/user_profile.html'


#     def get_context_data(self, **kwargs) :
#         context = super().get_context_data(**kwargs)
#         customer = self.request.user
#         address = Userdetail.objects.get
#         context['customer'] = customer
#         context['address'] = address
#         return context



# class Userdetail(LoginRequiredMixin,SuccessMessageMixin,CreateView):
#     model = Userdetail
#     form_class = userdetail
#     success_url = reverse_lazy('user:home')
#     template_name ='user_temp/userdetail_form.html'
#     error_message = 'Error saving the Doc, check fields below.'
#     success_message = 'Doc successfully created!'
#     login_url = 'home'



#     def form_valid(self, form):
#          form.instance.user_id = self.request.user
#          return super(Userdetail, self).form_valid(form)
    
#     def form_invalid(self, form):
#         messages.error(self.request, self.error_message)
#         return super().form_invalid(form)
        
@never_cache
def user_profile(request):
    if 'username' in request.session:
           email =  request.user.email
           user = request.user
           detail = myuser.objects.get(email = email)
           #detail = Userdetail.objects.filter(user_id  = user)
           try:
               
              cart_itemscount  = CartItem.objects.filter(user = request.user, is_active = True).count()
           except:
                 pass
          
           context ={
               
         
           'cart_itemscount':cart_itemscount,
           'detail':detail,
                    }
           
           return render(request,'user_temp/user_profile.html',context)
    #messages.info(request,'Please sign in')

    return redirect('user:user_signin')

@never_cache
def edit_profile(request):
        if 'username' in request.session:
            email =  request.user.email
            detail = myuser.objects.get(email = email)
      
            user = myuser.objects.get(email = email)
            form =  editprofile( instance=user)

            if request.method == 'POST':
                form = editprofile(request.POST, request.FILES,instance=user)
                if form.is_valid():
               
                    updated_email = form.cleaned_data['email']
                    form.save()
                    if updated_email == email:
                        
                        return redirect('user:user_profile')
                    else:
                        del request.session['username']
                        auth.logout(request)
                        messages.info(request,'please login with updated email')
                        return redirect('user:user_signin')
                else:
                   messages.info(request,'data not valid')
            context  ={
                'detail':detail,
                'form':form
            }
            return render(request,'user_temp/edit_profile.html',context)
        else:
            return redirect('user:user_signin')





# def edit_variant(request,pk):
#      if 'vendor' in request.session:
#          variant = Variant.objects.get(id =pk)
#          if request.method == 'POST':
#             form = Variantform(request.POST, request.FILES,instance=variant)
#             if form.is_valid():
#                 form.instance.vehicle_id = variant.vehicle_id  
#                 form.save()
#                 messages.success(request, ('VARIANT updated!'))
#             else:
#                  messages.success(request, ('Data is not valid!'))
#             return redirect('vendor:view_vehicles')
#          else:
#              form = Variantform( instance=variant)
#      return render(request,'vendor_temp/update_variant.html',{'form':form})


@cache_control(no_cache =True,  no_store =True)
def add_address(request):
    email =  request.user.email
    users = myuser.objects.get(email = email)
    #address  = Userdetail.objects.get(user_id = users.id)
    address  = Userdetail.objects.filter(user_id = users.id)
    context ={
           'users' :users,
           'address' :address,
                    }
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        mobile = request.POST['mobile']
        address1 = request.POST['address1']
        address2 = request.POST['address2']
        state = request.POST['state']
        country = request.POST['country']
        city = request.POST['city']
        user_id = users
        try:
            newaddress = Userdetail.objects.create(first_name = first_name,
                                               last_name=last_name,
                                               email = email,
                                               mobile=mobile,
                                               addressline1=address1,
                                               addressline2=address2,
                                               state = state,
                                               city =city,
                                               country=country,user_id=user_id)
            newaddress.save()
            messages.info(request,'Successfully created')
        except:
            messages.info(request,'Data not valid please try again')
    return render(request,'user_temp/add_address.html',context)
        

def delete_address(request,pk):
    address=Userdetail.objects.get(id=pk)
    address.delete()
    return redirect('user:add_address')

@cache_control(no_cache =True,  no_store =True)
def edit_address(request,pk):
    address=Userdetail.objects.get(id=pk)
    users = myuser.objects.get(email = request.user.email)
    context ={
           'users' :users,
           'address' :address,
                    }
    if request.method == 'POST':
        address.first_name = request.POST['first_name']
        address.last_name = request.POST['last_name']
        address.email = request.POST['email']
        address.mobile = request.POST['mobile']
        address.address1 = request.POST['address1']
        address.address2 = request.POST['address2']
        address.state = request.POST['state']
        address.country = request.POST['country']
        address.city = request.POST['city']
        address.save()
        return redirect('user:add_address')

    return render(request,'user_temp/edit_address.html',context)
      

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']
       

        try:
           user_obj = myuser.objects.get(email=email)
           token = str(uuid.uuid4())
       # profile_obj = myuser.objects.get(user = user_obj)
           user_obj.forgot_password_token = token
           user_obj.save()
           send_forget_password_mail(user_obj,token)
           messages.info(request,'an email is sent to your account')
        except:
             messages.info(request,'Email is not matching')
             
        return redirect('user:forgot_password')


    return render(request,'forget_password.html')

def change_password(request,token):
   
    try:
        profile_obj = myuser.objects.filter(forgot_password_token=token).first()
        print(profile_obj)
        context = {'user_id': profile_obj.id}

        if request.method == "POST":
            new_password = request.POST['password1']
            confirm_password = request.POST['password2']
            user_id = request.POST['user_id']


            if user_id is None:
                messages.info(request,'no user found')
                return redirect(f'/change_password/{token}/')
            if  new_password !=  confirm_password:
                messages.info(request,'password dosent match')
                return redirect(f'/change_password/{token}/')
            

            user_obj = myuser.objects.get(id = user_id)
            user_obj.set_password(new_password)
            user_obj.save()
            del request.session['username']
            return redirect('user:user_signin')

        
    except Exception as e:
        print(e)

    return render(request,'change_password.html',context)


#======================ORDER VIEWS =========================#\


def view_orders(request):
    user = request.user
    orders= Orders.objects.filter(user = user,).order_by('-id').exclude(status = 'Cancelled')
    print(orders)
   
    #order = Orders.objects.filter(user = request.user ).order_by('-id')
    context = {
        'orders': orders,
        
    }
    return render(request,'user_temp/orders.html',context)


def cancelled_orders(request):
       user = request.user
       orders = Orders.objects.filter(user = user,status = 'Cancelled')
     
       context = {
        'orders': orders,
           }
       return render(request,'user_temp/canceled_order.html',context)

def cancel_order(request,pk):
    if request.user.is_authenticated:
         orders= Orders.objects.get(id = pk)
         orders.status = 'Cancelled'
         orders.save()
         orderd_vehicle =OrderVehicle.objects.filter(order = orders.id)

         for i in orderd_vehicle:
             i.status = 'Cancelled'
             i.vehicles.remaining += i.quantity
             vehicle = Variant.objects.get(id=i.vehicles.id)
             vehicle.remaining += i.quantity
             vehicle.save()
             print( i.vehicles)
             i.save()
         return redirect('user:view_orders')
    return render(request,'user_temp/orders.html')

def order_details(request,pk):
    orderd_vehicle =OrderVehicle.objects.filter(order = pk)

    context = {
        'orderd_vehicle':orderd_vehicle
    }

    return render(request,'user_temp/order_detail.html',context)


def add_review(request,id):
    print('get')
    vehicle = Vehicles.objects.get(id=id)
    review = Review.objects.filter(user = request.user,product = vehicle)
    print(review)
    if request.method == 'POST':
        try:
            review = Review.objects.get(user = request.user,product = vehicle)
            print('updation')
            form    =   Reviewforms(request.POST , instance=review)
            form.save()
            messages.info(request,'Thank you... Your review has been updated')
            return redirect('review',id)
        except:
                form = Reviewforms(request.POST)
            
                if form.is_valid():
                    print('dfghjkgff')
                    data            =   Reviewforms()
                    data.rating     =   form.cleaned_data['rating']
                    data.subject    =   form.cleaned_data['subject']
                    data.review     =   form.cleaned_data['review']
                    form.instance.user = request.user
                    form.instance.product = vehicle
                    form.save()
                    messages.info(request, ('Review  added!'))
           
                else:
                    messages.info(request, ('Data is not valid!'))
                    return redirect('user:add_review',id=id)

      

    print(vehicle)
    print(vehicle.vehicle_name)
    context ={
    'vehicle':vehicle
         }

    return render(request,'user_temp/review.html',context)


def about(request):
      return render(request,'user_temp/about.html')
    





   

from django.shortcuts import render,redirect
from django.contrib import messages 
from django.contrib.auth import authenticate,login,logout
#from django.db import models
from user.models import myuser
from.models import Banner
from categories.models import Category
#from categories.forms import categoryform
from django.views.decorators.cache import cache_control
from.forms import Couponforms,Bannerforms
from Cartapp.models import Coupon
# Create your views here.

@cache_control(no_cache = True,must_revalidate = False,no_store = True)
def admin_signin(request):
    if 'admin' in request.session:
        return redirect('admin_panel')
    
    
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        
        try:
            admin = authenticate(email = email,password = password)

        except:
            admin = None
            pass
        if admin is not None:
            if admin.is_superadmin:
               request.session['admin']=email
               login(request,admin)
               return redirect('admin_panel')
            else:
                messages.info(request,'you are not an admin')
        else:
            messages.info(request,'invalid credential')
        
            
    return render(request,'admin_temp/admin_signin.html')


def admin_logout(request):
     if request.user.is_authenticated:
          del request.session['admin']
          logout(request)
     return redirect('admin_signin')

@cache_control(no_cache = True,must_revalidate = False,no_store = True)
def admin_panel(request):
     if 'admin' in request.session:
          return render(request,'admin_temp/admin_panel.html')
     return redirect('admin_signin')



# ======================vendor MANAGEMENT================================================================================================#

def vendor_mgmt(request):
    if 'admin' in request.session:
          vendors = myuser.objects.filter(is_staff=True,is_superadmin=False)
          return render(request,'admin_temp/vendor_detail.html',{'vendors':vendors})
    return redirect('admin_signin')
    

def block_vendor(request,pk):
    
    vendor = myuser.objects.get(id=pk)
    vendor.is_active = False
    vendor.save()
    print ('vendor is block')
    return redirect('vendor_mgmt')

def unblock_vendor(request,pk):
    vendor = myuser.objects.get(id=pk)
    vendor.is_active = True
    vendor.save()
    print('vendor  is active')
    return redirect('vendor_mgmt')


def delete_vendor(request,pk):
    vendor = myuser.objects.get(id=pk)
    vendor.delete()
    print('vendor deleted')
    return redirect('vendor_mgmt')
#==========================================================================user management==================================================#
def user_mgmt(request):
    users = myuser.objects.filter(is_staff=False,is_superadmin=False)
    return render(request,'admin_temp/user_detail.html',{'users':users})


def block_user(request,pk):
    user = myuser.objects.get(id =pk)
    user.is_active = False
    user.save()
    print('user blocked')
    return redirect('user_mgmt')


def unblock_user(request,id):
    user = myuser.objects.get(id= id)
    user.is_active  = True
    user.save()
    print('user is active')
    return redirect('user_mgmt')


def delete_user(request,pk):
    user = myuser.objects.get(id=pk)
    user.delete()
    print('user deleted')
    return redirect('user_mgmt')
    

#==============================================================CATEGORY MANAGEMENT============================================================#
def view_category(request):
    category = Category.objects.all()
    return render(request,'admin_temp/category.html',{'category':category})


def delete_category(request,pk):
    category = Category.objects.get(id =pk)
    category.delete()
    return redirect ('view_category')

def add_category(request):
    if request.method == 'POST':
        try:
            category_name = request.POST['category']
            image = request.FILES['image']
            description = request.POST['description']
            slug = request.POST['slug']
        except:
            messages.info(request,'form is not valid')
            return redirect('view_category')

    try:
        category = Category(
            category_name =category_name,
            description =description,
            image = image,
            slug = slug
        )

        category.save()
        return redirect('view_category')
    except:
    #    add_forms = categoryform(request.POST,request.FILES)
    #    if add_forms.is_valid():
    #        add_forms.save()
    #        return redirect('view_category')
    #    else:
    #         messages.info(request,'form is not valid please try again')
        return render(request,'admin_temp/add_category.html')

def edit_category(request,pk):
    edit = Category.objects.get(id=pk)
    if request.method == 'POST':
        try:
            category_name = request.POST['category']
            image = request.FILES['image']
            description = request.POST['description']
            slug = request.POST['slug']
            if image == '':
                messages.info(request,'images is empty')
                return redirect('view_category')
        except:
            messages.info(request,'form is not valid')
            return redirect('view_category')

    try:
        category= Category.objects.get(id=pk)
        category.category_name =category_name
        category.description =description
        category.image = image
        category.slug = slug
        category.save()
        return redirect('view_category')

    except:
        messages.info(request,'form is not valid please try again')
    return render(request,'admin_temp/edit_category.html',{'edit':edit})



#========================coupon management=================================#


def view_coupon(request):
    if 'admin' in request.session:
         coupon =  Coupon.objects.all().order_by( 'is_active')
         context = {
             'coupon':coupon
           }
    return render(request,'admin_temp/view_coupons.html',context)


def add_coupons(request):
    if 'admin' in request.session:
        forms = Couponforms(request.POST or None)
        
        if request.method == 'POST':
           if forms.is_valid:
               forms.save()
               messages.info(request,'Coupon added succusfully')
               return redirect('view_coupon') 
           else:
               messages.info(request,'Data not valid')
               return redirect('view_coupon') 
        context = {
            'forms':forms
        }
        return render(request,'admin_temp/add_coupon.html',context)
    
def block_coupon(request,id):
    coupon = Coupon.objects.get(id=id)
    coupon. is_active = False
    coupon.save()
    return redirect('view_coupon')

def un_block_coupon(request,id):
    coupon = Coupon.objects.get(id=id)
    coupon. is_active = True
    coupon.save()
    return redirect('view_coupon')

def del_coupon(request,id):
    coupon = Coupon.objects.get(id=id)
    coupon.delete()
    return redirect('view_coupon')



#=============================Banners===============#


def view_banner(request):
    if 'admin' in request.session:
        banner = Banner.objects.all()
        context = {
              'banner':banner
          }
        return render(request,'admin_temp/view_banner.html',context)



def add_banner(request):
    if 'admin' in request.session:
        form = Bannerforms()
        
        if request.method == 'POST':
           form = Bannerforms(request.POST, request.FILES)
           if form.is_valid:
               form.save()
               messages.info(request,'Banner added succusfully')
               return redirect('view_banner') 
           else:
               messages.info(request,'Data not valid')
               return redirect('view_banner') 
        context = {
            'form':form
        }
        return render(request,'admin_temp/banner.html',context)


    return render(request,'admin_temp/banner.html')


def delete_banner(request,id):
     banner = Banner.objects.get(id=id)
     banner.delete()
     return redirect('view_banner') 

def update_banner(request):
     
     if 'admin' in request.session:
         banner = Banner.objects.get(id=id)
         if request.method == 'POST':
            form = Bannerforms(request.POST, request.FILES,instance=banner)
            if form.is_valid():
                form.save()
                messages.success(request, ('Banner updated!'))
            else:
                 messages.success(request, ('Data is not valid!'))
            return redirect('view_banner')
         else:
             form = Bannerforms( instance=banner)

     return render(request,'vendor_temp/update_variant.html',{'form':form})
     
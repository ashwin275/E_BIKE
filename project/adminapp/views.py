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
from orders.models import OrderVehicle
from django.utils import timezone
from datetime import datetime
from django.db.models import Q
from django.http import JsonResponse
from django.core import serializers


from io import BytesIO
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter, landscape

from django.http import HttpResponse
from openpyxl import Workbook
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from datetime import date
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
        Date_input_two = datetime.today().date()
        Date_input_one = date.today().replace(day=1)
        current_month = datetime.now().strftime('%B')
        month = timezone.now().month
        current_month = datetime.now().strftime('%B')
        print(current_month)
        orders =[]
#=============cancelled and succuss orders of the month===================#
        Success_orders = OrderVehicle.objects.filter(order__created_at__month= month, status ='Delivered').count()
        cancelled_orders = OrderVehicle.objects.filter(order__created_at__month= month, status ='Cancelled').count()
        orders.append(Success_orders)
        orders.append(cancelled_orders)
        print(Success_orders)
        print(cancelled_orders)

#==================Top saled vehicle of the month=========================#
        vehicle_list = []
        sales = []
        Top_Saled_vehicle = OrderVehicle.objects.filter(order__created_at__month= month, status ='Delivered')

        for vehicle in Top_Saled_vehicle:
            if vehicle.vehicles.vehicle_id.vehicle_name in vehicle_list:
                i = vehicle_list.index(vehicle.vehicles.vehicle_id.vehicle_name)
                sales[i]+=vehicle.quantity
            else:
                vehicle_list.append(vehicle.vehicles.vehicle_id.vehicle_name)
                sales.append(vehicle.quantity)

        vehicle_dict = dict(zip(vehicle_list,sales))
        
        sorted_dict = dict(sorted(vehicle_dict.items(), key=lambda x: x[1], reverse=True))

        top_ten_vehicle = list(sorted_dict.keys())[:10]
        vehicles_sold = list(sorted_dict.values())[:10]

        


        context = {
            'orders':orders,
            'top_ten_vehicle':top_ten_vehicle,
            'vehicles_sold':vehicles_sold,
            'Date_input_one':Date_input_one,
            'Date_input_two':Date_input_two,
        }
          
          
        return render(request,'admin_temp/admin_panel.html',context)
     return redirect('admin_signin')

def filter_admin_dashboard(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

     #filter order and cancelled orders

    Success_orders = OrderVehicle.objects.filter(Q( status ='Delivered') & Q(order__created_at__date__gte =start_date)& Q(order__created_at__date__lte =end_date)).count()
    cancelled_orders = OrderVehicle.objects.filter(Q( status ='Cancelled') &Q(order__created_at__date__gte =start_date)& Q(order__created_at__date__lte =end_date)).count()
    print(Success_orders)
    print(cancelled_orders)
    

    #    filter top 10 vehicles   #
    
    vehicle_list=[]
    sales=[]
    Top_Saled_vehicle = OrderVehicle.objects.filter(Q( status ='Delivered')& Q(order__created_at__date__gte =start_date)& Q(order__created_at__date__lte =end_date))
    
    for vehicle in Top_Saled_vehicle:
        if vehicle.vehicles.vehicle_id.vehicle_name in vehicle_list:
            i = vehicle_list.index(vehicle.vehicles.vehicle_id.vehicle_name)
            sales[i]+=vehicle.quantity
        else:
            vehicle_list.append(vehicle.vehicles.vehicle_id.vehicle_name)
            sales.append(vehicle.quantity)

    vehicle_dict = dict(zip(vehicle_list,sales))
        
    sorted_dict = dict(sorted(vehicle_dict.items(), key=lambda x: x[1], reverse=True))

    top_ten_vehicle = list(sorted_dict.keys())[:10]
    vehicles_sold = list(sorted_dict.values())[:10]

    data = {
            
            'data': [Success_orders,cancelled_orders],
            'top_ten_vehicle':top_ten_vehicle,
            'vehicles_sold':vehicles_sold,
        }
    return JsonResponse(data)
    

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
        banner = Banner.objects.all().order_by('id')
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

def update_banner(request,id):
     
     
     if 'admin' in request.session:
         Banners = Banner.objects.all()
         print(Banners)
         banner = Banner.objects.get(id=id)
         if request.method == 'POST':
            form = Bannerforms(request.POST, request.FILES,instance=banner)
            if form.is_valid():
                banner_status = form.cleaned_data.get('status')
                print(banner_status)
                if banner_status == 'Banner-one':
                    for i in Banners:
                        if i.status == 'Banner-one':
                            i.status = 'Banner-Two'
                        else:
                            i.status = 'None'
                        i.save()
                elif banner_status == 'Banner-Two':
                    for i in Banners:
                        if i.status == 'Banner-Two':
                            i.status == 'Banner-one'
                        else:
                            i.status = 'None'
                            i.save()
                else:
                    for i in Banners:
                        if (i.status != 'Banner-Two') and (i.status != 'Banner-one'):
                            i.status = 'None'
                            i.save()

                form.save()
                messages.success(request, ('Banner updated!'))
            else:
                 messages.success(request, ('Data is not valid!'))
            return redirect('view_banner')
         else:
             form = Bannerforms( instance=banner)

     return render(request,'admin_temp/update_banner.html',{'form':form})
     




# def banner_status_change_main(request,id):
#     banner = Banner.objects.get(id=id)
#     banners = Banner.objects.all()
#     banner.status = 'Banner-one'
#     banners = Banner.objects.all()

#     for i in banners:
#         if i != banner and i.status != 'Banner-two':
#             i.status = 'None'
#             i.save()
#     banner.save()
#     return redirect('view_banner')

# def banner_status_change_sub(request,id):
#     banner = Banner.objects.get(id=id)
#     banners = Banner.objects.all()
#     banner.status = 'Banner-Two'
#     banners = Banner.objects.all()
#     for i in banners:
#         if i != banner and i.status != 'Banner-one':
#             i.status = 'None'
#             i.save()
#     banner.save()
#     return redirect('view_banner')

#============Sales report=======================#



def sales_report(request):
    if 'admin' in request.session:
        Date_input_two = datetime.today().date()
        Date_input_one = date.today().replace(day=1)
        month = timezone.now().month
        current_month = datetime.now().strftime('%B')
        print(current_month)
        total_revenue = 0
        orders = OrderVehicle.objects.filter( status ='Delivered',order__created_at__month= month).order_by('order__created_at')

        for order in orders :
            total_revenue += order.sub_total()
    
        
        context = {

              'orders':orders,
              'total_revenue':total_revenue,
              'Date_input_two':Date_input_two,
              'Date_input_one':Date_input_one,
           }
        return render(request,'admin_temp/sales_report.html',context)
    else:
        messages.info(request,"please login")
        return redirect ('vendor:vendor_signin')
    

def Excel_sales_report(request):
    # Generate sales report data
    month = timezone.now().month
    sales_data = [
        ['Order Id', 'Date', 'Vehicle', 'Color', 'Quantity', 'Price', 'Total'],
    ]
    orders = OrderVehicle.objects.filter( status ='Delivered',order__created_at__month= month).order_by('order__created_at')
  
    for order in orders:
        sub_total = order.quantity * order.price
        sales_data.append([
            order.order.order_number,
            order.order.created_at.strftime('%m/%d/%Y %I:%M %p'),
            order.vehicles.vehicle_id.vehicle_name,
            order.vehicles.color,
            order.quantity,
            order.price,
            sub_total
        ])
    
    # Create an Excel file and add the sales report data to it
    wb = Workbook()
    ws = wb.active
    ws.title = 'Sales Report'
    for row in sales_data:
        ws.append(row)

    # Offer the Excel file for download
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=sales_report.xlsx'
    wb.save(response)
    return response


def pdf_sales(request):
    month = timezone.now().month
    # Retrieve data for the report
    orders = OrderVehicle.objects.filter( status ='Delivered',order__created_at__month= month).order_by('order__created_at')

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer, pagesize=landscape(letter))
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="sales_report.pdf"'

   
    doc = SimpleDocTemplate(response, pagesize=letter)
    elements = []

   
    title_style = getSampleStyleSheet()["Title"]
    elements.append(Paragraph("Sales Report", title_style))
    date_style = getSampleStyleSheet()["Normal"]
    date_string = "Date:" + date.today().strftime("%m/%d/%Y")
    elements.append(Paragraph(date_string, date_style))

    # Create the table object and add it to the elements list
    data = [
        ['Order No', 'Date', 'Vehicle','Quantity','Color', 'Price', 'Total'],
    ]
    # Initialize the total variable
    grand_total = 0
    for sale in orders:
        total = sale.quantity*sale.price
        data.append([sale.order.order_number, sale.order.created_at.strftime("%d %b %Y"), sale.vehicles.vehicle_id.vehicle_name, sale.quantity,sale.vehicles.color, sale.price, total])
        grand_total += total

   # Add the grand total to the data list
    data.append(['', '', '', '', '', 'Grand Total', grand_total])
    table = Table(data)
    
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
    ]))
    elements.append(table)

   
    doc.build(elements)
    return response


# def filter_sales_report(request):
#     start_date = request.GET.get('start')
#     end_date = request.GET.get('end')

    

#     orders = OrderVehicle.objects.filter(Q( status ='Delivered') & Q(order__created_at__date__gte =start_date)& Q(order__created_at__date__lte =end_date))
    
#     print(orders)

#     data = [
#     {
#         'id': order.id,
#         'created_at': order.order.created_at.date(),
#         'order_number': order.order.order_number,
#         'vehicle_name': order.vehicles,
#         'vehicle_color': order.vehicles.color,
#         'vehicle_price':order.vehicles.price ,
#         'quantity': order.quantity,
#         'price': order.price,
#     }
#     for order in orders
# ]


#     return JsonResponse(data,safe=False)

                       
  
 



    
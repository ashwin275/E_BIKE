from django.shortcuts import render,redirect
from django.contrib import messages 
from django.http import HttpResponse
from openpyxl import Workbook
from django.http import JsonResponse,response
from django.contrib.auth import authenticate,login,logout
#from django.db import models
# import pandas as pd 
from django.contrib import messages,auth 
from django.db.models import Count,F , Sum

from user.models import myuser,Userdetail
from product.models import Vehicles,Variant
from categories.models import Category
from user.otp import check_otp,sentOTP
from django.views.decorators.cache import cache_control
from product.forms import Vehicleforms ,Variantform
from orders.models import OrderVehicle,Orders
from django.views.decorators.cache import never_cache
from django.utils import timezone
from datetime import datetime
from django.db.models import Q




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
#from django.contrib.auth.decorators import login_required

# Create your views here.


@cache_control(no_cache = True,must_revalidate = True,no_store = True)
def vendor_register(request):
    if 'vendor' in request.session:
        return redirect ('vendor:dash_board')

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

@never_cache
def vendor_signin(request):
    if 'vendor' in request.session:
        return redirect ('vendor:dash_board')
        
    if 'username' in request.session:
        del  request.session['username']
        auth.logout(request)
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        email_exsit =  myuser.objects.filter(email=email).exists()
      
        print(email_exsit)
     
        if email_exsit == False:
            messages.info(request,'email is incorect')
          
        else:
            vendor = authenticate(email=email,password=password)
            if vendor is not None and vendor.is_staff == True:
                print('true staff')
                if vendor.is_active == True:
                     print('true')
                     request.session['vendor']=email
                     login(request,vendor)
                     return redirect('vendor:dash_board')
                else:
                    messages.info(request,'Your account is inactive. Please contact the administrator.')

            else:
                messages.info(request,'invalid credential')
             
        
        return redirect('vendor:vendor_signin')
    return render (request,'vendor_temp/vendor_signin.html')


@never_cache
def dash_board(request):
    if 'vendor' in request.session:
        month = timezone.now().month
        Date_input_two = datetime.today().date()
      
        Date_input_one = date.today().replace(day=1)
       
        current_month = datetime.now().strftime('%B')
        print(current_month)
        vehicle = Vehicles.objects.filter(vendor_id = request.user)
#  sales chart for monthly saled vehicles and quantity
        vehicle_list = []
        quantity = []
        orders_chart =[]
        vehicle_order  = OrderVehicle.objects.filter( Q(vehicles__vehicle_id__vendor_id=request.user) & Q(status='Delivered') & Q(order__created_at__month = month))
        for vehicle in vehicle_order:
            if vehicle.vehicles.vehicle_id.vehicle_name in vehicle_list:
               i = vehicle_list.index(vehicle.vehicles.vehicle_id.vehicle_name)
               quantity[i] += vehicle.quantity
            else:
                vehicle_list.append(vehicle.vehicles.vehicle_id.vehicle_name)
                quantity.append(vehicle.quantity)
        print(vehicle_list,'121')
        print(vehicle_order,'1212')
    # charts for   cancelled orders and deliverd orders
        Success_orders = OrderVehicle.objects.filter( vehicles__vehicle_id__vendor_id = request.user,status ='Delivered',order__created_at__month = month).count()
        cancelled_orders = OrderVehicle.objects.filter( vehicles__vehicle_id__vendor_id = request.user,status ='Cancelled',order__created_at__month = month).count()
        orders_chart.append(Success_orders)
        orders_chart.append(cancelled_orders)
      
        context = {
           'vehicle_list':vehicle_list,
            'quantity':quantity,
            'orders_chart':orders_chart,
            'Date_input_two':Date_input_two,
            'Date_input_one':Date_input_one,
          }
        return render(request,'vendor_temp/chart_js.html',context)
    else:
        messages.info(request,"please login")
        return redirect ('vendor:vendor_signin')

def filter_dash_board(request):
    if 'vendor' in request.session:
        start_date_str = request.GET.get('start_date')
        end_date_str = request.GET.get('end_date')
       
        
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d')

        print(start_date)
        print(end_date)
        print('start-end')
      

        #filter sales and no #
        vehicle = Vehicles.objects.filter(vendor_id = request.user)
        vehicle_list = []
        quantity = []


        #vehicle_order  = OrderVehicle.objects.filter( Q(vehicles__vehicle_id__vendor_id = request.user,status ='Delivered') & Q(order__created_at__date__gte = start_date) & Q(order__created_at__date__lte = end_date))
      
 
        vehicle_order  = OrderVehicle.objects.filter( Q(vehicles__vehicle_id__vendor_id=request.user) & Q(status='Delivered') & Q(order__created_at__date__gte =start_date)& Q(order__created_at__date__lte =end_date)).order_by('order__created_at')
        print('vehicles', str(vehicle_order))
        for vehicle in vehicle_order:
            if vehicle.vehicles.vehicle_id.vehicle_name in vehicle_list:
               i = vehicle_list.index(vehicle.vehicles.vehicle_id.vehicle_name)
               quantity[i] += vehicle.quantity
            else:
                vehicle_list.append(vehicle.vehicles.vehicle_id.vehicle_name)
                quantity.append(vehicle.quantity)
        
        print(quantity)
        print(vehicle_list)
       

        # filter order and canceled orders #
        Success_orders = OrderVehicle.objects.filter( Q(vehicles__vehicle_id__vendor_id = request.user,status ='Delivered') & Q(order__created_at__date__gte =start_date)& Q(order__created_at__date__lte =end_date)).count()
        print(Success_orders)
        cancelled_orders = OrderVehicle.objects.filter( Q(vehicles__vehicle_id__vendor_id = request.user,status ='Cancelled') & Q(order__created_at__date__gte =start_date)& Q(order__created_at__date__lte =end_date) ).count()
        print(Success_orders)
        print(cancelled_orders)

        data = {
            
            'data': [Success_orders,cancelled_orders],
            'vehicle_list':vehicle_list,
            'quantity':quantity,

        }
        return JsonResponse(data)






# def search_dashboard(request):
#     if request.method == 'GET':
#             start_date_str = request.GET.get('start_date')
#             end_date_str = request.GET.get('end_date')

#             start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
#             end_date = datetime.strptime(end_date_str, '%Y-%m-%d')

#             vehicle = Vehicles.objects.filter(vendor_id = request.user)
#             vehicle_list = []
#             quantity = []
#             orders_chart =[]
#             vehicle_order  = OrderVehicle.objects.filter( vehicles__vehicle_id__vendor_id = request.user,)

#             context = {
#            'vehicle_list':vehicle_list,
#             'quantity':quantity,
#             'orders_chart':orders_chart,
#           }
#             return render(request,'vendor_temp/chart_js.html',context)




def vendor_logout(request):
         if 'vendor'  in request.session:
              del request.session['vendor']
              logout(request)
              return redirect('vendor:vendor_signin')



def vendor_profile(request):
    print('bnbnbmn')
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
        print('jkhkh')        
        try:

            #vendor = myuser.objects.get(email=request.user.email)
            vehicle = Vehicles.objects.filter(vendor_id = request.user ,is_available =True)
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
                 
            return redirect('vendor:view_vehicles')
    return render(request,'vendor_temp/add_vehicles.html',{'form':form})


# def add_offer(request,pk):
    
#     return render(request,'vendor_temp/offer.html',{'form':form})
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


def add_variant(request,pk):
    if 'vendor' in request.session:
        form = Variantform()
        vehicle = Vehicles.objects.get(id = pk)
       
        if request.method == 'POST':
            email = request.user.email
            vendor = myuser.objects.get(email =email)
            form = Variantform(request.POST, request.FILES)
            if form.is_valid():   
                form.instance.vehicle_id = vehicle 
                form.save()
                messages.success(request, ('VARIANT Added!'))
            else:
                 messages.success(request, ('Data is not valid!'))
            return redirect('vendor:view_vehicles')
    return render (request,'vendor_temp/add_variant.html',{'form':form})


def view_variant(request,pk):
    if 'vendor' in request.session:
        
        try:

            #vendor = myuser.objects.get(email=request.user.email)
            variant = Variant.objects.filter(  vehicle_id =pk).order_by('is_available')
            return render(request,'vendor_temp/view_variant.html',{'vehicle':variant})
        except:
            messages.success(request, ('Data is not valid!'))
            return redirect('vendor:view_vehicles')
    return render(request,'vendor_temp/view_variant.html')
     
def edit_variant(request,pk):
     if 'vendor' in request.session:
         
         variant = Variant.objects.get(id =pk)
       
       
         vehicle = Vehicles.objects.get(vehicle_name = variant.vehicle_id.vehicle_name)
         id = vehicle.id
         if request.method == 'POST':
            form = Variantform(request.POST, request.FILES,instance=variant)
            if form.is_valid():
                form.instance.vehicle_id = variant.vehicle_id  
                form.save()
                return redirect('vendor:view_variant',id)
            
            
         else:
             form = Variantform( instance=variant)
     return render(request,'vendor_temp/update_variant.html',{'form':form})

def delete_variant(request,id):
    vehicle= Variant.objects.get(id=id)
    vehicle.delete()
    return redirect('vendor:view_vehicles',)

def active_variant(request,pk):
    vehicle= Variant.objects.get(id=pk)
    vehicle.is_available = True
    vehicle.save()
    return redirect('vendor:view_vehicles',)

def de_active_variant(request,pk):
    vehicle= Variant.objects.get(id=pk)
    vehicle.is_available = False
    vehicle.save()
    return redirect('vendor:view_vehicles',)




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
def Orders_view(request):
    if 'vendor' in request.session:
         vendor = myuser.objects.get(email=request.user.email)
    # vehicle = Vehicles.objects.filter(vendor_id = vendor.id )
         orderd_vehicle =OrderVehicle.objects.filter(vehicles_id__vehicle_id__vendor_id =vendor.id,).order_by('-id').exclude(status ='Cancelled',)
         context = { 
          'orderd_vehicle':orderd_vehicle
           }
         return render (request,'vendor_temp/Orders.html',context)
    
def cancelled_orders(request):
       vendor = myuser.objects.get(email=request.user.email)
       orderd_vehicle =OrderVehicle.objects.filter(vehicles_id__vehicle_id__vendor_id =vendor.id,status ='Cancelled').order_by('-id')
       context = { 
          'orderd_vehicle':orderd_vehicle
           }
       return render (request,'vendor_temp/cancelled_orders.html',context)

def Returned_orders(request):
       vendor = myuser.objects.get(email=request.user.email)
       orderd_vehicle =OrderVehicle.objects.filter(vehicles_id__vehicle_id__vendor_id =vendor.id,status ='Returned').order_by('-id')
       context = { 
          'orderd_vehicle':orderd_vehicle
           }
       return render (request,'vendor_temp/cancelled_orders.html',context)

@cache_control(no_cache = True,must_revalidate = False,no_store = True)
def cancel_order(request,pk):
    if 'vendor' in request.session:
         orders= OrderVehicle.objects.get(id = pk)
         orders.status = 'Cancelled'
         orders.save()
         return redirect('vendor:Orders')


def status_change(request,pk):
    if 'vendor' in request.session:
         orders= OrderVehicle.objects.get(id = pk)
        
         Total_Order = Orders.objects.get(order_number = orders.order.order_number )
       

         Total_Order.status = 'order processing'
         Total_Order.save()
         if orders.status == 'Confirmed':
             orders.status = 'Shipped'
         elif orders.status == 'Shipped':
             orders.status = 'Out_for_delivery'
         elif orders.status == 'Out_for_delivery':
             orders.status = 'Delivered'
         else :
             orders.status = 'Returned'
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



#===========Sales report================#
@never_cache
def sales_report(request):
    if 'vendor' in request.session:
        month = timezone.now().month
        Date_input_two = datetime.today().date()
   
        Date_input_one = date.today().replace(day=1)
     
        #current_month = datetime.now().strftime('%B')
      
        total_revenue = 0
        #orders = OrderVehicle.objects.filter( vehicles__vehicle_id__vendor_id = request.user,status ='Delivered').order_by('order__created_at')
        orders  = OrderVehicle.objects.filter(Q( vehicles__vehicle_id__vendor_id = request.user) & Q(order__created_at__month =month) & Q(status ='Delivered')).order_by('order__created_at')
     
        for order in orders :
            total_revenue += order.sub_total()
    
        
        context = {

              'orders':orders,
              'total_revenue':total_revenue,
              'Date_input_one':Date_input_one,
              'Date_input_two':Date_input_two,
           }
        return render(request,'vendor_temp/sales report.html',context)
    else:
        messages.info(request,"please login")
        return redirect ('vendor:vendor_signin')

@never_cache
def search_sales_report(request):
    if 'vendor' in request.session:
        if request.method == 'GET':
            start_date_str = request.GET.get('start_date')
            end_date_str = request.GET.get('end_date')

            
     # Convert start_date and end_date to datetime objects

            start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
            Date_input_one =start_date
            Date_input_two =end_date

        

    # Create a Q object to filter based on the date range

            orders = OrderVehicle.objects.filter( Q(vehicles__vehicle_id__vendor_id=request.user) & Q(status='Delivered') & Q(order__created_at__date__gte =start_date)& Q(order__created_at__date__lte =end_date)).order_by('order__created_at')
            
            total_revenue = 0
              
            for order in orders :
                  total = order.sub_total()
                  total_revenue += total
            context = {
                     
               'orders':orders,
                'total_revenue':total_revenue,
                "Date_input_one":Date_input_one,
                'Date_input_two':Date_input_two,
              }
            return render(request,'vendor_temp/sales report.html',context)
        else:
            messages.info(request,"please login")
            return redirect ('vendor:vendor_signin')


def download_sales_report(request):
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')
    print(start_date_str)
    print(end_date_str)
        
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
    # Generate sales report data
    sales_data = [
        ['Order Id', 'Date', 'Vehicle', 'Color', 'Quantity', 'Price', 'Total'],
    ]
    orders  = OrderVehicle.objects.filter( Q(vehicles__vehicle_id__vendor_id=request.user)
                                           & Q(status='Delivered') 
                                           & Q(order__created_at__date__gte =start_date)
                                           & Q(order__created_at__date__lte =end_date)).order_by('order__created_at') 
  

    if orders:
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
    else:
        pass


#===============pdf download sales report==================#
def sales(request):
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')
    print(start_date_str)
    print(end_date_str)
        
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d')


    # Retrieve data for the report
    orders  = OrderVehicle.objects.filter( Q(vehicles__vehicle_id__vendor_id=request.user)
                                           & Q(status='Delivered') 
                                           & Q(order__created_at__date__gte =start_date)
                                           & Q(order__created_at__date__lte =end_date)).order_by('order__created_at') 
   

    if orders:
        # Create a buffer to receive PDF data
        buffer = BytesIO()

        # Create the PDF object, using the BytesIO object as its "file."
        doc = SimpleDocTemplate(buffer, pagesize=landscape(letter))
        # Set up the response
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="sales_report.pdf"'

        # Create the PDF object
        doc = SimpleDocTemplate(response, pagesize=letter)
        elements = []

        # Add the report title and date to the elements list
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

        # Build the PDF document and return the response
        doc.build(elements)
        return response
   





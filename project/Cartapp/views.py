from django.shortcuts import render,redirect,get_object_or_404
from product.models import Vehicles,Variant
from .models import Cart,CartItem,Coupon,Used_Coupon
from user.models import Userdetail,myuser
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

import razorpay
from django.conf import settings
# Create your views here.



def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def cart_count(request):
    cart_itemscount  = CartItem.objects.filter(user = request.user, is_active = True).count()
    count = {'cart_itemscount':cart_itemscount}
    return JsonResponse(count)


def add_to_cart(request,pk,):

    vehicle = Variant.objects.get(id=pk)

    if vehicle.remaining == 0:
         messages.info(request,'Vehicle out of stock')
         return redirect('Cartapp:cart')
    if 'username' in request.session:
        is_cart_item_exist = CartItem.objects.filter(product=pk,user=request.user).exists()

        if is_cart_item_exist:
            cartitem = CartItem.objects.get(user = request.user,product = vehicle)
            cartitem.quantity += 1
            if vehicle.remaining < cartitem.quantity :
                 messages.info(request,'vehicle out of stock')
                 return redirect('Cartapp:cart')
            cartitem.save()
            #return redirect('Cartapp:cart')
        else:
            cartitem = CartItem.objects.create(product=vehicle,user = request.user,quantity=1)
            cartitem.save()

        print("my-user")
        return redirect('Cartapp:cart')
    else:
        messages.info(request,'Please sign in')
        return redirect('user:user_signin')
        # try:
        #     cart=Cart.objects.get(cart_id=_cart_id(request))
        #     print(cart+'helo')

        # except Cart.DoesNotExist:
        #     cart=Cart.objects.create(
        #         cart_id=_cart_id(request)
        #     )
        #     cart.save()
        #     print(cart)
        #     print('33333333333')
        # try:
        #     cart_item=CartItem.objects.get(product=vehicle,cart = int(cart))
        #     cart_item.quantity += 1
        #     cart_item.save()
        # except:
        #     cart_item=CartItem.objects.create(
        #         product=vehicle,
        #         quantity=1,
        #         cart_id=cart
        #     )
        #     cart_item.save()
        # print("no-user")
        





def update_cart_quantity(request):
   
  if request.method == 'POST':
    total = 0
    item_id = request.POST['item_id']
    quantity = int(request.POST['quantity'])
    cart_item = CartItem.objects.get(id=item_id)
    cart = CartItem.objects.filter(user = request.user)
    
    vehicle_in_stock = cart_item.product.remaining

    print(vehicle_in_stock)
    if vehicle_in_stock < quantity:
        print('error message')
        return JsonResponse({'status': 'error', 'message': 'sorry only  '+ str(vehicle_in_stock) + '  vehicle in stock'})
    
    cart_item.quantity = quantity
    cart_item.save()
    print( 'qty after'+str(cart_item.quantity))
    print('jbbmnb')
    for item in cart:
               total += item.product.price*item.quantity
    
    Sub_total = cart_item.product.price*cart_item.quantity
    tax = round(((18 * total) / 100))
    grand_total = (total+tax)
    booking_price = 100000
    return JsonResponse({
      'quantity': quantity,
      'total': total,
      'tax':tax,
      'grand_total':grand_total,
      'booking_price':booking_price,
      'Sub_total':Sub_total,
    })
  else:
    return JsonResponse({})




def cart_count(request):
    try:
      cart_itemscount  = CartItem.objects.filter(user = request.user, is_active = True).count()
      count = {'cart_itemscount':cart_itemscount}
    except:
        cart_itemscount = 0
        count = {'cart_itemscount':cart_itemscount}
    return JsonResponse(count)

        
        
def cart(request, total = 0, total_qty =0 , tax =0,cart_items=None, grand_total =0, reduction =0):
    if 'username' in request.session:
            cart_items = CartItem.objects.filter(user= request.user).order_by("-id")
            for item in cart_items:
               total += item.product.price*item.quantity
               total_qty  +=item.quantity
            
            in_stock = cart_items
            tax = round(((18 * total) / 100))
            grand_total = ((total+tax)-reduction)
            booking_price = 100000
            context = {
                    'cart_items':cart_items,
                     'total':total,
                     'total_qty':total_qty,
                      'tax':tax,
                      'grand_total':grand_total,
                      
                      'booking_price':booking_price,   
                    }
            return render(request,'cart/cart.html',context)
    
    
    else:
         messages.info(request,'Please sign in')
         return redirect('user:user_signin')

   



def remove_cart_item(request,pk):

    vehicle = get_object_or_404(Variant,id = pk)
    if request.user.is_authenticated:
        cart_item=CartItem.objects.get(product=vehicle,user=request.user)
    else:
        cart=Cart.objects.get(cart_id=_cart_id(request))
        cart_item=CartItem.objects.get(product=vehicle,cart_id=cart)

    cart_item.delete()
    return redirect('Cartapp:cart')


def decrement_quantity(request,pk):
    vehicle = get_object_or_404(Variant,id = pk)
    try:
        if request.user.is_authenticated:
            cart_item =CartItem.objects.get(product=vehicle,user=request.user)
        else:
            cart=Cart.objects.get(cart_id=_cart_id(request))
            cart_item=CartItem.objects.get(product=vehicle,cart_id=cart)

        if cart_item.quantity>1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()

    except:
        pass

    return redirect('Cartapp:cart')


def checkout(request):
    email =  request.user.email
    user = myuser.objects.get(email = email)

   
    if request.user.is_authenticated:
        

        address = Userdetail.objects.filter(user_id = user.id)
        context = {
             'address':address
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
            user_id = user
            print(first_name)
            print(last_name)
            print(email)
            print(mobile)
            print(address1)
            print(address2)
            print(state)
            print(country)
            print(city)
            print(state)
            print(user_id)

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
                newaddress.default = True
                newaddress.save()
                others = Userdetail.objects.filter(user_id = user.id).exclude(id = newaddress.id )
                for i in others:
                    i.default = False
                    i.save()
                    print('done')
                    messages.info(request,'Successfully created')
                    return redirect('Cartapp:review_order')
            except:
                    
                    messages.info(request,'Data not valid please try again')
                    return redirect('Cartapp:checkout')
    return render(request,'cart/checkout.html',context)

def address_default(request,id):
    email =  request.user.email
    user = myuser.objects.get(email = email)
    address = Userdetail.objects.get(id=id)
    address.default = True
    address.save()
    others = Userdetail.objects.filter(user_id = user.id).exclude(id = id )

    for i in others:
        i.default = False
        i.save()
        print('done')

    return redirect('Cartapp:review_order')
    


@login_required
def coupon_apply(request):
  
   discount = 0
   if request.method =='POST':
       
        coupon_code = request.POST.get('coupon_code')
        total = request.POST.get('total')
        tax = request.POST.get('tax')
       # reduction = request.POST.get('reduction')
        grand_total = request.POST.get('grandtotal')
        booking_price = request.POST.get('booking_price')
        balance = request.POST.get('balance')
        try:
           coupon_exist = Coupon.objects.get(coupon_code = coupon_code , is_active = True )
           print(coupon_exist)
        except:
            return JsonResponse({'status': 'error', 'message': 'Coupon is not valid.'})
        if 'coupon_code' in request.session:
            return JsonResponse({'status': 'error', 'message': 'You already used one coupon.'})

        if coupon_exist:
            try:
                print('exist')
                if Used_Coupon.objects.get(coupon=coupon_exist,user=request.user):
                    print('coupon used')
                  
                    return JsonResponse({'status': 'error', 'message': 'Coupon already used please try with other one .'})
            except:
                   print('noooo')
                   request.session['coupon_code'] = coupon_code
                   discount = coupon_exist.discount
                   print(discount)

                   grand_total = (int(total)+int(tax))- int(discount )
                   booking_price = int(round( grand_total/4))
                   balance = int(grand_total)-int(booking_price)
                   print('session created')
                  
                   return JsonResponse({
                       'status': 'success',
                         'message': 'Coupon applied successfully!',
                         'grand_total':str(grand_total),
                         'booking_price':str(booking_price),
                         'balance':str(balance),
                         'discount':str(discount),
                         })
                  

            

def cancel_coupon(request):
    if 'coupon_code' in request.session:
        del request.session['coupon_code']
        print('coupon deleted')
        return JsonResponse({'status': 'success', 'message': 'Coupon Deleted!'})
    else:
        return JsonResponse({'status': 'error', 'message': 'No coupon found in session.'})

    

    

def review_order(request, total = 0 , total_qty =0 , tax =0,cart_items=None, grand_total =0, reduction =0):
    user = myuser.objects.get(email = request.user.email)

    if request.user.is_authenticated:
            if 'coupon_code' in request.session:
                coupon_code = request.session['coupon_code']
                coupon = Coupon.objects.get(coupon_code =coupon_code)
                reduction = coupon.discount
                #messages.success(request,'Coupon applyed')
                print( reduction)
            else:
                reduction=0

            cart_items = CartItem.objects.filter(user= request.user).order_by("-id")
            cart_itemscount  = CartItem.objects.filter(user = request.user, is_active = True).count()
            address = Userdetail.objects.get(user_id = user.id, default = True)
          
            for item in cart_items:
               total += item.product.price*item.quantity
               total_qty  +=item.quantity
            tax = round(((18 * total) / 100))
            grand_total = ((total+tax)-reduction)
            booking_price = 100000
            balance = grand_total- booking_price

            #===========razor pay ==============#
            client = razorpay.Client(auth = (settings.KEY,settings.SECRET))
            payment = client.order.create({'amount':booking_price *100,'currency': 'INR',})
            print(payment)
            context = {
                    'cart_items':cart_items,
                     'total':total,
                     'total_qty':total_qty,
                      'tax':tax,
                      'grand_total':grand_total,
                      'cart_itemscount':cart_itemscount,
                      'booking_price':booking_price,  
                      'address': address,
                      'user':user,
                      'reduction':reduction,
                      'balance':balance,
                      'payment':payment
                    }
            
    return render(request,'cart/order_review.html',context)




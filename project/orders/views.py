from django.shortcuts import render,redirect
from Cartapp.models import CartItem,Coupon
from user.models import Userdetail,myuser
from . models import Orders,OrderVehicle,Payment
import random
from django.views.decorators.csrf import csrf_exempt
import razorpay
from django.conf import settings
client = razorpay.Client(auth = (settings.KEY,settings.SECRET))


# Create your views here.


def Book_now(request):
    total = 0
    booking_price = 0
    cart_items =None
    tax = 0
    grand_total =0
    total_qty =0
    balance = 0
    
    user = request.user

    user_id = myuser.objects.get(id = request.user.id)
    cart_items=CartItem.objects.filter(user=user.id)
    address =Userdetail.objects.filter(default = True).get(user_id =  user.id)
    if not cart_items:
          return redirect('Cartapp:cart')


    order_number = random.randint(100000,999999)
    if 'coupon_code' in request.session:
                coupon_code = request.session['coupon_code']
                coupon = Coupon.objects.get(coupon_code =coupon_code)
                reduction = coupon.discount
    else:
         reduction =0   
    for item in cart_items:
          total += item.product.price*item.quantity
          total_qty  +=item.quantity
          tax = round(((18 * total) / 100))
          grand_total = ((total+tax)-reduction)
          booking_price = 100000
          balance = grand_total- booking_price
          rem = item.product.remaining -item.quantity
          

    orders = Orders.objects.create(user = request.user,
                                    address = address,
                                    order_number =  order_number,
                                    order_total = total_qty, 
                                      pending_amount = balance,
                                       tax = tax,
                                        discount_price = reduction,
                                        )
    orders.save()
    for i in cart_items:
        OrderVehicle.objects.create(
                 order = orders,
                  vehicles = i.product,
                 quantity = i.quantity,
                 price = i.product.price,
                 user = request.user
           )
        i.delete()

    get_order =  Orders.objects.get(order_number =order_number)
    ordered_item = OrderVehicle.objects.filter(order = get_order,user = request.user)
    print(ordered_item)
    if 'payment_id'  in request.session:
          payment_id = request.session['payment_id']
          payment = Payment.objects.create(user = request.user,payment_id=payment_id, payment_method='razorpay',status='Booking amount paid',amount_paid =booking_price )
          payment.save()
          get_order.pending_amount =  balance
          del request.session['payment_id'] 
    else:
          payment = Payment.objects.create(user = request.user, payment_method='COD',status='NOT PAID',amount_paid ='NOT PAID' )
          payment.save()
    if 'coupon_code' in request.session:
          del request.session['coupon_code']
    context = {
            ' user_id': user_id,
            'address':address,
            'get_order':get_order,
            'ordered_item':ordered_item,
            'tax':tax,
            'grand_total': grand_total,
            'total':total,
            'booking_price':booking_price,
            'balance': balance,
            'payment':payment,
       }
    
    return render(request,'cart/order_success.html',context)

@csrf_exempt
def handlerrequest(request):
      # user = request.user
      # request.session['user'] = user
      if request.method == "POST":
            try:
                  payment_id = request.POST.get('razorpay_payment_id','')
                  order_id = request.POST.get('razorpay_order_id','')
                  signature = request.POST.get('razorpay_signature','')
                  params_dict = {
                        'razorpay_payment_id':payment_id ,
                        'razorpay_order_id': order_id ,
                        'razorpay_signature':signature
                  }
            except:
                  pass
            try:
                client.utility.verify_payment_signature(params_dict)
            except:
                  return redirect ('Orders:order_success')
            
            
            request.session['payment_id'] = payment_id
           
            # print(user)
            # print("HEHEHEH")
            # saving payment detail
           # payment = Payment.objects.create(user = request.user,payment_id=payment_id, payment_method='razorpay',status='Completed')

            return redirect('Orders:Book_now')
                  


def payment_failed(request):
      return render(request,'cart/payment_failed.html')
# @csrf_exempt
# def payment_success(request):
#       print('njknjnf')
#       return render(request,'cart/payment_failed.html')


 
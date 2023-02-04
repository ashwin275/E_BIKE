from django.shortcuts import render
from Cartapp.models import CartItem,Coupon
from user.models import Userdetail,myuser
from . models import Orders,OrderVehicle
import random

# Create your views here.


def Book_now(request):
    total = 0
    quantity = 0
    cart_items =None
    tax = 0
    grand_total =0
    total_qty =0
    balance = 0
    user = request.user
    user_id = myuser.objects.get(id = request.user.id)
    cart_items=CartItem.objects.filter(user=user.id)
    address =Userdetail.objects.filter(default = True).get(user_id =  user_id)

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
          booking_price = round(( grand_total/2))
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


#     new_order = Orders.objects.get( order_number = order_number)
#     print(new_order)
#     ordered_items = OrderVehicle.objects.filter(order = orders)
#     print(ordered_items)
    get_order =  Orders.objects.get(order_number =order_number)
    ordered_item = OrderVehicle.objects.filter(order = get_order,user = request.user)
    print(ordered_item)
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
            'balance': balance

       }

   

    return render(request,'cart/order_success.html',context)



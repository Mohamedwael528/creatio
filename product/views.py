from pyexpat.errors import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Sum
from django.db import transaction
from decimal import Decimal, ROUND_HALF_UP



from .models import Product, CartItem, Order, OrderItem
from .serializers import ProductSerializers
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt




# Create your views here.

def products(request):
    x = {'products':Product.objects.all()}
    return render(request, 'home/index.html', x)

def product_detail(request, product_id):
    product = Product.objects.get(id=product_id)
    return render(request, 'home/product.html', {'product': product})



@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        size = request.POST.get('size')
        quantity = request.POST.get('quantity')
        
        # التحقق من أن الحجم والكمية تم تقديمهم
        if size and quantity:
            cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product, size=size)
            if not created:
                cart_item.quantity = quantity
            cart_item.save()

    return redirect('cart_detail')


@login_required
def cart_detail(request):
    cart_items = CartItem.objects.filter(user=request.user)
    return render(request, 'home/cart_detail.html', {'cart_items': cart_items})


@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    cart_item.delete()
    return redirect('cart_detail')


@login_required
@login_required
@transaction.atomic
def place_order(request):
    cart_items = CartItem.objects.filter(user=request.user)

    if request.method == 'POST':
        order = Order.objects.create(user=request.user)

        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                product_name=cart_item.product.name,
                price=cart_item.product.price,
                size=cart_item.product.size,
                quantity=cart_item.quantity,
                image=cart_item.product.main_image,
                user=request.user
            )
        
        cart_items.delete()
        return redirect('order_confirmation', order.id)

    return redirect('cart_detail')


@login_required
@csrf_exempt
@require_POST
def cancel_order(request, order_id):
    user = request.user
    order_items = OrderItem.objects.filter(order_id=order_id, user=user)
    
    if order_items.exists():
        order_items.delete()
        return JsonResponse({"message": "Order items deleted successfully."}, status=200)
    
    return JsonResponse({"message": "No order items found."}, status=404)




@login_required
def order_confirmation(request, order_id):
    user = request.user 
    order = get_object_or_404(Order, id=order_id)
    order_items = OrderItem.objects.filter(order=order)
    total = Decimal(order_items.aggregate(total_price=Sum('price'))['total_price'] or 0)

    total = total.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    if request.method == 'POST':
        for order_item in order_items:
            order_item.first_name = request.POST.get('first_name')
            order_item.last_name = request.POST.get('last_name')
            order_item.company_name = request.POST.get('company_name', '')
            order_item.address = request.POST.get('address')
            order_item.email = request.POST.get('email')
            order_item.phone = request.POST.get('phone')
            order_item.additional_info = request.POST.get('additional_info', '')
            order_item.save()
        
        return redirect('succecful_orderd')

    return render(request, 'home/order_confirmation.html', {'order': order, 'order_items': order_items, 'total': total, 'order_id': order_id})


def orders(request):
    user = request.user  # الحصول على معلومات المستخدم الحالي
    orders = OrderItem.objects.filter(user=user)
    total = Decimal(orders.aggregate(total_price=Sum('price'))['total_price'] or 0)
    total = total.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    context = {'orders': orders, 'user': user, 'total': total}
    return render(request, 'home/orders.html', context)

def succecful(request):
    return render(request,'home/succecful_order.html')



# views.py
import stripe
from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from home.models import CartItem
from decimal import Decimal, ROUND_HALF_UP
from home.models import Order, OrderItem
from django.contrib.auth.decorators import login_required


stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required
def payment_page(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = 0
    
    for item in cart_items:
        price = item.product.price
        discount = item.product.discount
        
        if not item.product.discount:
            total_price+=item.product.price*item.quantity
        else:
            total_price+=(price-price*(Decimal(discount)/Decimal(100)))*item.quantity #Discount in percentage
        
    context = {
        'stripe_public_key' : settings.STRIPE_PUBLIC_KEY,
        'total_price' : total_price.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP),
    }
    return render(request, 'payment/payment.html', context)


@login_required
@csrf_exempt
def create_payment_intent(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = 0
    order = Order.objects.create(user=request.user)
    order.save()
    for item in cart_items:
        price = item.product.price
        discount = item.product.discount
        if not item.product.discount:
            total_price+=item.product.price*item.quantity
            order_item = OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price*item.quantity
            )
            order_item.save()
        else:
            discounted_price = (price-price*(Decimal(discount)/Decimal(100)))*item.quantity #Discount in percentage
            total_price+=discounted_price
            order_item = OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=discounted_price
            )
            order_item.save()
            
    order.total = total_price
    order.save()   
    
    if request.method == 'POST':
        try:
            
            # Create a PaymentIntent with the order amount and currency
            intent = stripe.PaymentIntent.create(
                amount=int(total_price*100),  # The price in cents
                currency='usd',
                payment_method_types=['card'],  # Accept Visa, MasterCard, etc.
                metadata={'order_id': order.id},
            )
            return JsonResponse({'clientSecret': intent['client_secret']})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=403)

@csrf_exempt
def stripe_webhook(request):
    if request.method == 'POST':
        payload = request.body
        sig_header = request.headers.get('Stripe-Signature')
        endpoint_secret = settings.STRIPE_ENDPOINT_SECRET

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, endpoint_secret
            )
        except ValueError:
            return JsonResponse({'error': 'Invalid payload'}, status=400)
        except stripe.error.SignatureVerificationError:
            return JsonResponse({'error': 'Invalid signature'}, status=400)

        # Handle the event type you care about
        if event['type'] == 'payment_intent.succeeded':
            payment_intent = event['data']['object']
            order_id = payment_intent['metadata']['order_id']
            order = Order.objects.get(id=order_id)
            user_id = order.user.id
            order.payment_status = True
            order.save()
            for item in CartItem.objects.filter(user=user_id):
                item.delete()
            
            print(f"PaymentIntent was successful: {payment_intent}")
            # Example: update order status in the database

        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

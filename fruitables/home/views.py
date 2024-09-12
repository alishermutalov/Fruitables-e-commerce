from django.conf import settings
from django.shortcuts import render,  get_object_or_404, redirect
from django.views.generic import (
    ListView,
)
from django.views import View
from django.views.generic.detail import DetailView
from .models import Product, Category, CartItem
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.db.models import Q
from django.db.models import Count
from decimal import Decimal, ROUND_HALF_UP
from django.contrib.auth.mixins import LoginRequiredMixin


class HomeView(ListView):
    model = Product
    template_name = 'home/index.html'   
    context_object_name = 'products'
    paginate_by = 8  

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get all categories to display in the navigation
        categories = Category.objects.all()
        context["categories"] = categories
        
        # Attempt to get user-specific information
        try:
            # Retrieve the user's cart items
            cart_items_quantity = CartItem.objects.filter(user=self.request.user).count()
            user = User.objects.get(id=self.request.user.id)
            context["user"] = user
            context["cart_items_quantity"] = cart_items_quantity
        except Exception as e:
            print(e)  # For debugging purposes, you may want to log this instead of printing

        # Retrieve the category slug and set it in the context if present
        category_slug = self.kwargs.get('category_slug') or self.kwargs.get('slug')
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            context['category'] = category
        else:
            context['category'] = None

        return context

    def get_queryset(self):
        # Get products filtered by category slug if available
        category_slug = self.kwargs.get('category_slug') or self.kwargs.get('slug')
        if category_slug:
            return Product.objects.filter(category__slug=category_slug)
        return Product.objects.all()


class ShopView(ListView):
    paginate_by = 6 # Display 8 products per page
    model = Product
    template_name = 'home/shop.html'
    context_object_name = 'products'
    def get_context_data(self, **kwargs):
        discounted_products = Product.objects.filter(Q(discount__gt = 0))
        context = super().get_context_data(**kwargs)
        categories = categories = Category.objects.annotate(product_count=Count('products'))
        context["categories"] = categories
        try:
            cart_items_quantity = CartItem.objects.filter(user=self.request.user).count()
            user = User.objects.get(id=self.request.user.id)
            context["user"] = user
            context["discounted_products"] = discounted_products
            context["cart_items_quantity"] = cart_items_quantity
        except Exception as e:
            print(e)
        return context   

      
class ProductDetailView(DetailView):
    model = Product
    template_name = 'home/shop-detail.html'
    context_object_name = 'product'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get categories with product counts
        categories = Category.objects.annotate(product_count=Count('products'))
        context["categories"] = categories

        try:
            # Get all products (both discounted and non-discounted)
            products = Product.objects.all()
            
            # Get the current user
            user = self.request.user

            # Count the cart items for the current user
            cart_items_quantity = CartItem.objects.filter(user=user).count()
            
            # Add additional context
            context["user"] = user
            context["products"] = products
            context["cart_items_quantity"] = cart_items_quantity

            # Adding total prices of each product (with or without discount)
            cart_items = CartItem.objects.filter(user=user)
            total_price_list = []
            for item in cart_items:
                if item.product.discount:
                    discounted_price = item.product.price * (1 - item.product.discount / 100)
                    total_price = discounted_price * item.quantity
                else:
                    total_price = item.product.price * item.quantity
                total_price_list.append(total_price)

            # Adding total price to the context
            context['total_price_list'] = total_price_list
            
        except Exception as e:
            # Log the exception or handle it as needed
            print(f"Error fetching data: {e}")
            
        return context    


class AddToCartView(LoginRequiredMixin,View):
    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        quantity = int(request.POST.get('quantity', 1))  # Get the quantity from the form

        # Check if the cart item already exists
        cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)

        if not created:
            # If the item already exists in the cart, increment the quantity
            cart_item.quantity += quantity
        else:
            # Otherwise, set the quantity as the new value
            cart_item.quantity = quantity

        cart_item.save()

        return redirect('cart_detail')


class CartDetailView(LoginRequiredMixin, ListView):
    model = CartItem
    template_name = 'home/cart.html'
    context_object_name = 'cart_items'

    def get_queryset(self):
        # Fetch the cart items for the logged-in user
        return CartItem.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.all()
        context["categories"] = categories

        try:
            cart_items = self.get_queryset()  # Reuse the queryset method
            total = Decimal('0.00')  # Initialize total as a Decimal

            for item in cart_items:
                price = item.product.price  # Assume this is already a Decimal

                if item.product.discount:
                    # Calculate discounted price using Decimal
                    discount = Decimal(item.product.discount) / Decimal('100')
                    discounted_price = price * (Decimal('1') - discount)
                    total_price = discounted_price * Decimal(item.quantity)
                else:
                    # Regular price
                    total_price = price * Decimal(item.quantity)

                total += total_price  # Add to the total amount

            # Round total to 2 decimal places
            total = total.quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)

            # Fetch the logged-in user
            user = self.request.user
            
            # Count the number of items in the user's cart
            cart_items_quantity = CartItem.objects.filter(user=self.request.user).count()

            # Pass the total and other variables to the context
            context["total"] = total
            print("TOTAL: ", context["total"])
            context["user"] = user
            context["cart_items_quantity"] = cart_items_quantity
        except Exception as e:
            # Handle any errors that may occur
            print(f"Error calculating cart total: {e}")
            context["error"] = "There was an issue retrieving your cart details."

        return context
    

class UpdateCartQuantityView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        cart_item_id = request.POST.get('cart_item_id')
        action = request.POST.get('action')
        
        cart_item = get_object_or_404(CartItem, id=cart_item_id, user=request.user)
           
        if action == 'increase':
            cart_item.quantity += 1
        elif action == 'decrease':
            cart_item.quantity -= 1
            if cart_item.quantity <= 0:
                cart_item.delete()
                return JsonResponse({'success': True, 'removed': True})
        
        cart_item.save()
        return JsonResponse({
                'success': True,
                'quantity': cart_item.quantity,
                'price_per_item': cart_item.product.price,
                'removed': False
            })
     
def contact_view(request):
    cart_items_quantity = CartItem.objects.filter(user=request.user).count()
    context = {}
    context["user"] = request.user
    context["cart_items_quantity"] = cart_items_quantity
    return render(request, 'home/contact.html', context)

def custom_404_view(request, exception=None):
    return render(request, 'home/404.html', status=404)


from django.urls import path
from .views import( 
                   HomeView,
                   ProductDetailView,
                   CartDetailView, 
                   AddToCartView, 
                   UpdateCartQuantityView,
                   ShopView, 
                   contact_view,
                   )
from django.views.generic import TemplateView



urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('shop/', ShopView.as_view(), name='shop'),
    path('category/<slug:category_slug>/', HomeView.as_view(), name='product_list_by_category'),
    path('product/detail/<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('cart/', CartDetailView.as_view(), name='cart_detail'),
    path('cart/add/<int:pk>/', AddToCartView.as_view(), name='add_to_cart'),
    path('cart/update-quantity/', UpdateCartQuantityView.as_view(), name='update_cart_quantity'),
    path('contact/', contact_view, name='contact'),
    path('order-success/', TemplateView.as_view(template_name='order_success.html'), name='payment_success'),
]

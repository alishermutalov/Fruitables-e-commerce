from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Category, Product, CartItem, Order, OrderItem
from decimal import Decimal

User = get_user_model()

class CategoryModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(category_name='Electronics')
    
    def test_category_str(self):
        self.assertEqual(str(self.category), 'Electronics')
    
    def test_category_slug_auto_generated(self):
        self.assertEqual(self.category.slug, 'electronics')


class ProductModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(category_name='Electronics')
        self.product = Product.objects.create(
            category=self.category,
            product_name='Laptop',
            description='A high-quality laptop',
            price=Decimal('1000.00'),
            discount=10
        )
    
    def test_product_str(self):
        self.assertEqual(str(self.product), 'Laptop')
    
    def test_product_slug_auto_generated(self):
        self.assertEqual(self.product.slug, 'laptop')
    
    def test_get_discounted_price(self):
        cart_item = CartItem.objects.create(product=self.product, quantity=2)
        total_price = cart_item.get_total_price()
        self.assertEqual(total_price, Decimal('1800.00'))  # 10% discount on 1000 for 2 items


class CartItemModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.category = Category.objects.create(category_name='Electronics')
        self.product = Product.objects.create(
            category=self.category,
            product_name='Phone',
            description='A smartphone',
            price=Decimal('500.00')
        )
        self.cart_item = CartItem.objects.create(user=self.user, product=self.product, quantity=3)

    def test_cart_item_str(self):
        self.assertEqual(str(self.cart_item), '3 x Phone for testuser')

    def test_cart_item_total_price(self):
        self.assertEqual(self.cart_item.get_total_price(), Decimal('1500.00'))


class OrderModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.order = Order.objects.create(user=self.user, total=Decimal('100.00'))
    
    def test_order_str(self):
        self.assertEqual(str(self.order), f'Order {self.order.id} by testuser')
    
    def test_order_default_status(self):
        self.assertEqual(self.order.status, 'pending')


class OrderItemModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.category = Category.objects.create(category_name='Electronics')
        self.product = Product.objects.create(
            category=self.category,
            product_name='Tablet',
            description='A tablet device',
            price=Decimal('200.00')
        )
        self.order = Order.objects.create(user=self.user, total=Decimal('600.00'))
        self.order_item = OrderItem.objects.create(
            order=self.order, 
            product=self.product, 
            quantity=3, 
            price=Decimal('200.00')
        )
    
    def test_order_item_str(self):
        self.assertEqual(str(self.order_item), '3 x Tablet in Order {}'.format(self.order.id))
    
    def test_order_item_total_price(self):
        self.assertEqual(self.order_item.total_price, Decimal('600.00'))

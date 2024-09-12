from django import template
from decimal import Decimal, ROUND_HALF_UP

register = template.Library()

@register.filter
def discounted_price(price, discount):
    # Convert price and discount to Decimal
    price = Decimal(price)
    discount = Decimal(discount)
    
    # Calculate the discounted price
    discounted = price - (price * (discount / Decimal(100)))
    
    # Quantize to 2 decimal places
    return discounted.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

@register.filter
def multiply(value, arg):
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return ''
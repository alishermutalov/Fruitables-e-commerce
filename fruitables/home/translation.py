from modeltranslation.translator import register, TranslationOptions, translator
from .models import Product, Category

#1-usul
@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = ['product_name','description']
    
    
@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ['category_name',]
    
       

 
#2-usul   
# translator.register(Product, ProductTranslationOptions)
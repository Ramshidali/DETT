from django.contrib import admin
from products.models import ProductCategory,ProductVariant,Product,ProductImage,Unit,Brand,RecentSearches,GstCodes

admin.site.register(ProductCategory)
admin.site.register(ProductVariant)
admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(Unit)
admin.site.register(Brand)
admin.site.register(RecentSearches)
admin.site.register(GstCodes)

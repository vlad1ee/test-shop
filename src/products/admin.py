from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
from products.models import Product, Color, Size, Category, Cart


admin.site.register(
    Category,
    DraggableMPTTAdmin,
    list_display=(
        'tree_actions',
        'indented_title',
    ),
    list_display_links=(
        'indented_title',
    ),
)

admin.site.register(Product)
admin.site.register(Color)
admin.site.register(Size)
admin.site.register(Cart)

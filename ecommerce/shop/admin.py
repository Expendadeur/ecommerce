from django.contrib import admin
# pyrefly: ignore [missing-import]
from .models import Category, Product, ProductReview, Commande, ContactMessage, Newsletter, Wishlist

admin.site.site_header = "Administration Janvier-Shop"
admin.site.site_title = "Janvier-Shop Admin"
admin.site.index_title = "Tableau de bord d'administration"

@admin.register(Category)
class AdminCategory(admin.ModelAdmin):
    list_display = ('name', 'slug', 'icon', 'date_added')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


class ProductReviewInline(admin.TabularInline):
    model = ProductReview
    extra = 0
    readonly_fields = ('date_added',)


@admin.register(Product)
class AdminProduct(admin.ModelAdmin):
    list_display = ('title', 'category', 'price', 'discount_price', 'stock', 'rating', 'is_featured', 'date_added')
    list_filter = ('category', 'is_featured', 'date_added')
    search_fields = ('title', 'description', 'brand')
    list_editable = ('price', 'discount_price', 'stock', 'is_featured')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ProductReviewInline]


@admin.register(ProductReview)
class AdminProductReview(admin.ModelAdmin):
    list_display = ('product', 'name', 'rating', 'date_added')
    list_filter = ('rating', 'date_added')
    search_fields = ('name', 'email', 'comment', 'product__title')


@admin.register(Commande)
class AdminCommande(admin.ModelAdmin):
    list_display = ('order_number', 'nom', 'email', 'phone', 'ville', 'pays', 'total', 'status', 'payment_method', 'date_commande')
    list_filter = ('status', 'payment_method', 'pays', 'date_commande')
    search_fields = ('order_number', 'nom', 'email', 'phone', 'address', 'ville')
    list_editable = ('status',)
    readonly_fields = ('order_number', 'date_commande')


@admin.register(Wishlist)
class AdminWishlist(admin.ModelAdmin):
    list_display = ('product', 'user', 'date_added')
    list_filter = ('date_added',)
    search_fields = ('product__title', 'user__username', 'user__email')


@admin.register(ContactMessage)
class AdminContactMessage(admin.ModelAdmin):
    list_display = ('nom', 'email', 'sujet', 'date_envoye', 'lu')
    list_filter = ('lu', 'date_envoye')
    search_fields = ('nom', 'email', 'sujet', 'message')
    list_editable = ('lu',)


@admin.register(Newsletter)
class AdminNewsletter(admin.ModelAdmin):
    list_display = ('email', 'date_abonne')
    search_fields = ('email',)

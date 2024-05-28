from django.contrib import admin
from .models import Cake, Chief, Person, Order, Category, Tag, User, Review


@admin.register(Cake)
class CakeAdmin(admin.ModelAdmin):
    list_display = ('name', 'filling', 'price', 'weight', 'order_count')
    search_fields = ('name', 'filling')
    list_filter = ('price', 'weight')


@admin.register(Chief)
class ChiefAdmin(admin.ModelAdmin):
    list_display = ('username', 'address', 'number', 'logo')
    search_fields = ('username', 'address', 'number')


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('username', 'address', 'number')
    search_fields = ('username', 'address', 'number')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('count', 'design', 'create_date', 'due_date', 'chief', 'client', 'product')
    search_fields = ('design', 'create_date')
    list_filter = ('create_date', 'due_date')


admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(Review)
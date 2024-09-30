from django.contrib import admin
from .models import *

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ['id','username','email']

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name','category','price']

admin.site.register(User, UserAdmin)
admin.site.register(Product, ProductAdmin)

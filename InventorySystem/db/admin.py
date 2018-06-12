from django.contrib import admin
from .models import Items, Employee, ItemAssignment
# Register your models here.
admin.site.register(Items)
admin.site.register(Employee)
admin.site.register(ItemAssignment)

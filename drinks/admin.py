from django.contrib import admin
from .models import Drink, Category
from import_export.admin import ImportExportModelAdmin
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget, DateWidget
from django.contrib.auth.models import User  

class DrinkResource(resources.ModelResource):
    name = fields.Field(
        column_name='Drink',
        attribute='name', 
    )
    quantity = fields.Field(
        column_name='Quantity',
        attribute='quantity',
    )
    price = fields.Field(
        column_name='Price',
        attribute='price',
    )
    category = fields.Field(
        column_name='Category',
        attribute='category',
        widget=ForeignKeyWidget(Category, 'name')  # Use the 'name' field of the Category model
    )
    created_date = fields.Field(
        column_name='Created Date',
        attribute='created_date',
        widget=DateWidget(format='%Y-%m-%d %H:%M:%S')  # Format the date
    )
    last_updated = fields.Field(
        column_name='Last Updated',
        attribute='last_updated',
        widget=DateWidget(format='%Y-%m-%d %H:%M:%S')  # Format the date
    )
    employee = fields.Field(
        column_name='Employee',
        attribute='employee',
        widget=ForeignKeyWidget(User, 'username')  # Use the 'username' field of the User model
    )

    class Meta:
        model = Drink
        fields = ('name', 'quantity', 'price', 'category', 'created_date', 'last_updated', 'employee')
        export_order = ('name', 'quantity', 'price', 'category', 'created_date', 'last_updated', 'employee')


class RecordAdmin(ImportExportModelAdmin):
    resource_class = DrinkResource 
    list_display = ['name', 'quantity', 'price', 'category', 'created_date', 'last_updated', 'employee']

# Register models
admin.site.register(Category)
admin.site.register(Drink, RecordAdmin)
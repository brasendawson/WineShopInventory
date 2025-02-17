from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget, DateWidget
from .models import Drink, EditHistory, Category
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
        widget=ForeignKeyWidget(Category, 'name')
    )
    created_date = fields.Field(
        column_name='Created Date',
        attribute='created_date',
        widget=DateWidget(format='%Y-%m-%d %H:%M:%S')
    )
    last_updated = fields.Field(
        column_name='Last Updated',
        attribute='last_updated',
        widget=DateWidget(format='%Y-%m-%d %H:%M:%S')
    )
    employee = fields.Field(
        column_name='Employee',
        attribute='employee',
        widget=ForeignKeyWidget(User, 'username')
    )

    class Meta:
        model = Drink
        fields = ('name', 'quantity', 'price', 'category', 'created_date', 'last_updated', 'employee')
        export_order = ('name', 'quantity', 'price', 'category', 'created_date', 'last_updated', 'employee')

class EditHistoryInline(admin.TabularInline):
    model = EditHistory
    extra = 0
    readonly_fields = ('editor', 'edit_time', 'changes')


class DrinkAdmin(ImportExportModelAdmin):
    resource_class = DrinkResource
    list_display = ('name', 'quantity', 'price', 'category', 'created_date', 'last_updated', 'employee')
    inlines = [EditHistoryInline]

@admin.register(EditHistory)
class EditHistoryAdmin(admin.ModelAdmin):
    list_display = ('drink', 'editor', 'edit_time', 'changes')
    list_filter = ('editor', 'edit_time')
    search_fields = ('drink__name', 'editor__username')

    def get_queryset(self, request):
        if request.user.is_superuser or request.user.is_staff:
            return EditHistory.objects.all()
        return EditHistory.objects.filter(editor=request.user)

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

admin.site.register(Drink, DrinkAdmin)
admin.site.register(Category)
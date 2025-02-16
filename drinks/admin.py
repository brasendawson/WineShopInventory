from django.contrib import admin
from .models import Drink, Category
from import_export.admin import ImportExportModelAdmin

admin.site.register(Category)
class RecordAdmin(ImportExportModelAdmin):
    list_display = ['name', 'quantity', 'price', 'category', 'created_date', 'last_updated', 'creator']


admin.site.register(Drink, RecordAdmin)



# Register your models here.

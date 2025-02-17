from django.db import models
from django.contrib.auth.models import User

class Drink(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    employee = models.ForeignKey(User, on_delete=models.CASCADE, related_name="drinks")
    def __str__(self):
        return self.name
    
    def log_edit(self, editor, changes=None):
        # Log the edit in the EditHistory model
        EditHistory.objects.create(drink=self, editor=editor, changes=changes)

class Category(models.Model):
	name = models.CharField(max_length=200)

	class Meta:
		verbose_name_plural = 'categories'

	def __str__(self):
		return self.name

class EditHistory(models.Model):
    drink = models.ForeignKey(Drink, on_delete=models.CASCADE, related_name='edit_history')
    editor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    edit_time = models.DateTimeField(auto_now_add=True)
    changes = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Edit Histories'

    def __str__(self):
        return f'{self.drink.name} edited by {self.editor.username} at {self.edit_time}'





# Create your models here.

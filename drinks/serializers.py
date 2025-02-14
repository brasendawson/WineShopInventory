from rest_framework import serializers
from .models import Drink

class DrinkSerializer(serializers.ModelSerializer):
    creator = serializers.ReadOnlyField(source='creator.username')

    class Meta:
        model = Drink
        fields = [
            'id' , 'name' , 'quantity', 'price' , 'category' , 'created_date' , 'last_updated' , 'creator' 
        ]

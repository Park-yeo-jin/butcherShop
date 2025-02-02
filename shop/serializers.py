from rest_framework import serializers
from .models import Category, Product

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'content',
            'stock',
            'price',
            'category',
            'image',
        ]

    def get_category(self, obj):
        return obj.Lcategory.name + ' > ' + obj.Scategory.name
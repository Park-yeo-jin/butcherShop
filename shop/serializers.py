from rest_framework import serializers
from .models import Category, Product

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        # fields = '__all__'
        fields = [
            'id',
            'name',
            'parent',
        ]

class ProductSerializer(serializers.ModelSerializer):
    # category = serializers.SerializerMethodField()
    Lcategory = CategorySerializer()
    Scategory = CategorySerializer()

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'content',
            'stock',
            'price',
            'Lcategory',
            'Scategory',
            'image',
        ]

    def get_category(self, obj):
        return obj.Lcategory.name + ' > ' + obj.Scategory.name
    
# class LoginUserSerializer(serializers.Serializer):
#     username = serializers.CharField(help_text="아이디")
#     password = serializers.CharField(help_text="패스워드")
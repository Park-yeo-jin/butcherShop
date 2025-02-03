from django.db import models

class Category(models.Model):
    name = models.CharField(max_length = 100)
    categoryType = models.CharField(max_length = 10)
    parent = models.ForeignKey('self', null = True, blank = True, on_delete = models.CASCADE)

    def __str__(self):
        return self.name
    
class CategoryView(Category):
    class Meta:
        proxy = True

    
class Product(models.Model):
    name = models.CharField(max_length = 100)
    content = models.TextField(null = True)
    # 재고
    stock = models.IntegerField()
    price = models.DecimalField(max_digits = 10, decimal_places = 2)
    # 대분류
    Lcategory = models.ForeignKey(Category, on_delete = models.CASCADE, related_name='products_L')
    # 소분류
    Scategory = models.ForeignKey(Category, on_delete = models.CASCADE, related_name = 'products_S')
    image = models.ImageField(upload_to = 'products/')

    def __str__(self):
        return self.name
    
class Customer(models.Model):
    name = models.CharField(max_length = 100)
    password = models.CharField(max_length = 100)
    email = models.EmailField(unique = True)
    phone = models.CharField(max_length = 15)

    def __str__(self):
        return self.name

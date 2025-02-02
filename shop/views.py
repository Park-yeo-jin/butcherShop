
from rest_framework import viewsets
# from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.http import JsonResponse
from rest_framework import filters
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.permissions import AllowAny

class ShopViewSet(viewsets.ViewSet):

    def list(self, request):
        return JsonResponse({"message": "Hello, world!"})

    def retrieve(self, request, pk=None):
        return JsonResponse({"message": "Hello, world!"})
    
    def delete(self, request, pk=None):
        return JsonResponse({"message": "Hello, world!"})
    
    def update(self, request, pk=None):
        return JsonResponse({"message": "Hello, world!"})
    
    def create(self, request):
        return JsonResponse({"message": "Hello, world!"})
    
# @swagger_auto_schema(
#         method="get",
#         operation_description="정육점 관리자페이지",
#         manual_parameters=[
#             openapi.Parameter(
#                 name="question_id",
#                 in_=openapi.IN_QUERY,
#                 type=openapi.TYPE_INTEGER,
#                 required=True,
#             ),
#             openapi.Parameter(
#                 name="shop_id",
#                 in_=openapi.IN_QUERY,
#                 type=openapi.TYPE_INTEGER,
#             )
#         ],
        
#         # responses={
#         #     200: 'result.html',
#         # },
#         tags=["정육점"]
#     )
# @api_view(["GET"])

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter]
    permission_classes = [AllowAny]
    search_fields = ['name']

    def get_queryset(self):
        queryset = super().get_queryset()
        l_category_id = self.request.query_params.get('l_category')
        s_category_id = self.request.query_params.get('s_category')
        search = self.request.query_params.get('search')

        filters = {}
        if l_category_id:
            filters['Lcategory__name__contains'] = l_category_id
        if s_category_id:
            filters['Scategory__name__contains'] = s_category_id
        if search:
            filters['name__contains'] = search
        
        return queryset.filter(**filters)
    
    @swagger_auto_schema(
        operation_description="상품 목록 조회",
        manual_parameters=[
            openapi.Parameter(
                name="l_category",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                required=False,
            ),
            openapi.Parameter(
                name="s_category",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                required=False,
            ),
            openapi.Parameter(
                name="search",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                required=False,
            )
        ],
        tags=["상품"]
    )
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return JsonResponse(serializer.data, safe=False)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return JsonResponse(serializer.data)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return JsonResponse(serializer.data)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return JsonResponse(serializer.data)
    
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return JsonResponse(serializer.data)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return JsonResponse({"message": "삭제되었습니다."})

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data.update({"username": self.user.username})
        data.update({"email": self.user.email})
        return data

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
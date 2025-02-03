
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
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action

# class ShopViewSet(viewsets.ViewSet):

#     def list(self, request):
#         return JsonResponse({"message": "Hello, world!"})

#     def retrieve(self, request, pk=None):
#         return JsonResponse({"message": "Hello, world!"})
    
#     def delete(self, request, pk=None):
#         return JsonResponse({"message": "Hello, world!"})
    
#     def update(self, request, pk=None):
#         return JsonResponse({"message": "Hello, world!"})
    
#     def create(self, request):
#         return JsonResponse({"message": "Hello, world!"})
    
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
    # filter_backends = [filters.SearchFilter]
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter)
    # filterset_fields = ['Lcategory', 'Scategory']
    filterset_fields = ['Lcategory', 'Scategory']
    permission_classes = [AllowAny]
    search_fields = ['name']
    ordering = ['id']

    @action(detail=False, methods=['get'])

    def get_queryset(self):
        queryset = super().get_queryset()
        Lcategory_Id = self.request.query_params.get('Lcategory')
        Scategory_Id = self.request.query_params.get('Scategory')
        search = self.request.query_params.get('search')

        filters = {}

        if Lcategory_Id:
            filters['Lcategory__name__contains'] = Lcategory_Id
        if Scategory_Id:
            filters['Scategory__name__contains'] = Scategory_Id
        # if search:
        #     filters['name__contains'] = search
        
        return queryset.filter(**filters)
    
    @swagger_auto_schema(
        operation_description="상품 목록 조회",
        manual_parameters=[
            openapi.Parameter(
                name="Lcategory",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                required=False,
            ),
            openapi.Parameter(
                name="Scategory",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                required=False,
            ),
            # openapi.Parameter(
            #     name="search",
            #     in_=openapi.IN_QUERY,
            #     type=openapi.TYPE_STRING,
            #     required=False,
            # )
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
    
    def search(self, request):
        query = request.query_params.get('q', None)
        
        if query:
            products = Product.objects.filter(name__icontains=query)
        else:
            products = Product.objects.all()
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)
    
# class ProductFilter(viewsets.ModelViewSet):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
#     filterset_fields = ['Lcategory', 'Scategory']  
#     search_fields = ['name']
#     ordering_fields = ['id']
#     ordering = ['id']

# class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
#     def get_token(cls, user):
#         token = super().get_token(user)
#         return token
     
#     def validate(self, attrs):
       
#         username = attrs.get("username")
#         password = attrs.get("password")

#         user = authenticate(username=username, password=password)

#         if not user :
#             if self.user_model.objects.filter(username=username).exists():
#                 raise AuthenticationFailed("비밀번호가 올바르지 않습니다.", code="invalid_password")
#             else:
#                 raise AuthenticationFailed("존재하지 않는 사용자입니다.", code="user_not_found")
#         if not user.is_active:
#             raise AuthenticationFailed("사용할 수 없는 계정입니다.", code="inactive_user")

#         return super().validate(attrs)

# class CustomTokenObtainPairView(TokenObtainPairView):
#     serializer_class = CustomTokenObtainPairSerializer

#     @swagger_auto_schema(
#         operation_summary="토큰 발급",
#         operation_description="토큰 발급합니다.",
#         request_body=openapi.Schema(
#             type=openapi.TYPE_OBJECT,
#             properties={
#                 'username': openapi.Schema(type=openapi.TYPE_STRING, description='사용자명'),
#                 'password': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_PASSWORD, description='비밀번호'),
#             },
#             required=['username', 'password']
#         ),
#         responses={
#             200: openapi.Schema(
#                 type=openapi.TYPE_OBJECT,
#                 properties={
#                     'access': openapi.Schema(type=openapi.TYPE_STRING, description='액세스 토큰'),
#                     'refresh': openapi.Schema(type=openapi.TYPE_STRING, description='리프레시 토큰'),
#                 }
#                             ),
#             400: openapi.Response(description="존재하지 않는 사용자", examples={"application/json": {"detail": "존재하지 않는 사용자입니다."}}),
#             401: openapi.Response(description="잘못된 비밀번호", examples={"application/json": {"detail": "비밀번호가 틀렸습니다."}}),
#         }
#     )
#     def post(self, request, *args, **kwargs):
#         return super().post(request, *args, **kwargs)

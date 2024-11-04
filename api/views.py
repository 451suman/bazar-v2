from msilib.schema import ListView
from urllib import response
from django.contrib.auth.models import Group, User
from rest_framework import permissions, viewsets, status

from api.serializers import GroupSerializer, ProductSerializer, ReviewSerializer, UserSerializer
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView

from api.serializers import CategorySerializer
from ecomapp.models import Category, Product, Review


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all().order_by('name')
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by('-id')
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [permissions.AllowAny()]
        return super().get_permissions()
    

class ProductsViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by('-id')
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [permissions.AllowAny()]
        return super().get_permissions()

class ProductListByCategoryViewSet(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(
            category =self.kwargs['category_id']
        )

        return queryset

# category id comes from urls ['category_id']
   

# class ReviewViewSet(ListAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer
#     permission_classes = [permissions.AllowAny]  # Fixed typo from permissions_class

#     def get_queryset(self):
#         # Filter reviews by product ID (pk)
#         queryset = super().get_queryset()
#         queryset = queryset.filter(product_id=self.kwargs['pk'])  # Correctly use product_id
#         return queryset

class ReviewViewSet(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, pk, *args, **kwargs):
        reviews = Review.objects.filter(product_id=self.kwargs['pk'])
        serialized_data = ReviewSerializer(reviews, many=True).data
        return response(serialized_data, status= status.HTTP_200_OK)
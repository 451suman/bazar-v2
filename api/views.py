from msilib.schema import ListView
from urllib import response
from django.contrib.auth.models import Group, User
from rest_framework import permissions, viewsets, status

from api.serializers import (
    GroupSerializer,
    ProductSerializer,
    ReadReviewSerializer,
    # ReviewSerializer,
    UserSerializer,
    WriteReviewSerializer,
)
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView

from api.serializers import CategorySerializer
from ecomapp.models import Category, Customer, Product, Review
from rest_framework.views import APIView
from rest_framework.views import Response
from rest_framework import status, permissions


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """

    queryset = Group.objects.all().order_by("name")
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by("-id")
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [permissions.AllowAny()]
        return super().get_permissions()


class ProductsViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by("-id")
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
        queryset = queryset.filter(category=self.kwargs["category_id"])

        return queryset


# views.py


from django.shortcuts import get_object_or_404


# class ReviewViewSet(APIView):
# permission_classes = [permissions.IsAuthenticated]

# def get(self, request, product_id, *args, **kwargs):
#     # Fetch product and related reviews
#     product = get_object_or_404(Product, id=product_id)
#     reviews = Review.objects.filter(product=product).order_by("-created_at")
#     serializer = ReviewSerializer(reviews, many=True)
#     return Response(serializer.data, status=status.HTTP_200_OK)

# # post not working
# def post(self, request, product_id, *args, **kwargs):
#     # Ensure that the product exists
#     product = get_object_or_404(Product, id=product_id)

#     # Ensure the user has an associated customer object
#     try:
#         customer = request.user.customer
#     except Customer.DoesNotExist:
#         return Response(
#             {"detail": "User does not have an associated customer."},
#             status=status.HTTP_400_BAD_REQUEST,
#         )

#     # Attach the product and customer to the request data
#     request.data["product"] = product.id
#     request.data["customer"] = customer.id  # Set the customer ID

#     # Serialize the data
#     serializer = ReviewSerializer(data=request.data)

#     if serializer.is_valid():
#         # Save the review to the database
#         serializer.save()

#         # Return the created review with a 201 CREATED status
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

#     # If the data is not valid, return the errors
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReviewViewSet(viewsets.ViewSet):

    def list(self, request, product_id):
        queryset = Review.objects.filter(product=product_id)
        serializer = ReadReviewSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, product_id):
        # Include the product_id in the data since it's not in the request body
        data = request.data.copy()
        data["product"] = product_id

        # Serialize the data
        serializer = WriteReviewSerializer(data=data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

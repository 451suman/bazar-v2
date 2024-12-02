from django.contrib.auth.models import Group, User
from rest_framework import serializers

from ecomapp.models import Category, Customer, Product, Review


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username"]


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ["id", "name"]


class CustomerSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Customer
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class ProductNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "title"]


class CustomerNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ["user", "full_name"]


class WriteReviewSerializer(serializers.ModelSerializer):
    customer = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Review
        fields = [
            "id",
            "rating",
            "review_text",
            "product",
            "customer",
        ]
        extra_kwargs = {
            "id": {"read_only": True},
            "customer": {"read_only": True},
        }

    def validate_customer(self, value):
        try:
            return value.customer  # Assume `User` has a related `Customer` instance.
        except AttributeError:
            raise serializers.ValidationError(
                "The current user is not associated with a Customer instance."
            )


class ReadReviewSerializer(serializers.ModelSerializer):
    product = ProductNameSerializer()
    customer = CustomerNameSerializer()

    class Meta:
        model = Review
        fields = [
            "id",
            "rating",
            "review_text",
            "created_at",
            "product",
            "customer",
        ]
        read_only_felds = fields

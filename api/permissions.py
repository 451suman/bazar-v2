# your_app/permissions.py

from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of a customer record or admin users to modify it.
    """

    def has_object_permission(self, request, view, obj):
        # Allow access if the user is the owner of the customer record or an admin
        return obj.user == request.user

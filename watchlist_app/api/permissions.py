from math import perm
from rest_framework import permissions

"""
    permission for 'if a user is admin he can edit'
    otherwise for normal users they have the right for reading only.
"""


class AdminOrReadOnly(permissions.IsAdminUser):

    def has_permission(self, request, view):

        if request.method in permissions.SAFE_METHODS:
            # Check permissions for read-only requests
            return True
        else:
            return bool(request.user and request.user.is_staff)


class ReviewUserOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            # Check permissions for read-only requests
            return True

        else:
            # Check permissions for write requests
            return obj.review_user == request.user

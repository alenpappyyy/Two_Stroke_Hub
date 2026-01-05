from rest_framework import permissions

class IsSeller(permissions.BasePermission):
    """Allow access only to users with role 'Seller' or superuser."""
    def has_permission(self, request, view):
        user = request.user
        return bool(user and user.is_authenticated and (user.is_superuser or (user.role and user.role.name.lower() == 'seller')))

class IsAdminRole(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return bool(user and user.is_authenticated and (user.is_superuser or (user.role and user.role.name.lower() == 'admin')))

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes model instance has `seller` or `user` attribute.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True
        user = request.user
        if not user or not user.is_authenticated:
            return False
        if user.is_superuser:
            return True
        # common owner fields: seller or user
        owner = getattr(obj, 'seller', None) or getattr(obj, 'user', None)
        return owner == user

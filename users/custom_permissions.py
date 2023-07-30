from rest_framework.permissions import IsAuthenticated, IsAdminUser

class CustomPermissionMixin:
    def get_permissions(self):
        if self.request.method in ('DELETE', 'POST','PUT'):
            return [IsAdminUser(), ]
        else:
            return [IsAuthenticated(), ]
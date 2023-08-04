
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import update_session_auth_hash
from change_password.serializer import PasswordChangeSerializer

class PasswordChangeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PasswordChangeSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            old_password = serializer.data.get("old_password")
            new_password = serializer.data.get("new_password")

            # Check old password
            if not user.check_password(old_password):
                return Response({"error": "Invalid old password."}, status=status.HTTP_400_BAD_REQUEST)

            # Set new password and update session auth hash
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)  # To keep the user logged in

            return Response({"message": "Password changed successfully."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# views.py

from django.contrib.auth.models import User
from users.views import CustomUser
from django.core.mail import send_mail
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from django.urls import reverse
from rest_password.serializer import PasswordResetSerializer

class PasswordResetAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        
        if serializer.is_valid():
            
            email = serializer.validated_data['email']
            user = get_object_or_404(CustomUser, email=email)
            # Generate the custom password reset link
            reset_url = reverse('custom_password_reset_confirm', kwargs={'uidb64': user.id, 'token': default_token_generator.make_token(user)})
           
            print(reset_url)

            # Send the password reset email
            subject = 'Password Reset'
            message = f'Click the following link to reset your password: {reset_url}'
            from_email = 'your_email@gmail.com'
            recipient_list = [email]
            send_mail(subject, message, from_email, recipient_list)

            return Response({'message': 'Password reset link sent successfully.'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetConfirmAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, uidb64, token):
        try:
            user_id = int(uidb64)
            user = get_object_or_404(User, id=user_id)
        except (ValueError, User.DoesNotExist):
            return Response({'error': 'Invalid password reset link.'}, status=status.HTTP_400_BAD_REQUEST)

        if default_token_generator.check_token(user, token):
            password = request.data.get('new_password')
            user.set_password(password)
            user.save()
            return Response({'message': 'Password reset successful.'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid password reset link.'}, status=status.HTTP_400_BAD_REQUEST)

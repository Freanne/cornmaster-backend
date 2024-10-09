from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import CustomUser, Agriculteur, ExpertAgricole, Administrateur
from .serializers import CustomUserSerializer, AgriculteurSerializer, ExpertAgricoleSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate

class InscriptionView(APIView):
    def post(self, request):
        data = request.data
        user_serializer = CustomUserSerializer(data=data)
        
        if user_serializer.is_valid():
            user = user_serializer.save()

            # Vérifier le rôle de l'utilisateur et créer les détails spécifiques
            if data['role'] == 'agriculteur':
                agriculteur_data = {
                    'user': user.id,
                    'type_ferme': data.get('type_ferme'),
                    'localisation': data.get('localisation')
                }
                agriculteur_serializer = AgriculteurSerializer(data=agriculteur_data)
                if agriculteur_serializer.is_valid():
                    agriculteur_serializer.save()

            elif data['role'] == 'expert':
                expert_data = {
                    'user': user.id,
                    'specialisation': data.get('specialisation'),
                }
                expert_serializer = ExpertAgricoleSerializer(data=expert_data)
                if expert_serializer.is_valid():
                    expert_serializer.save()

            elif data['role'] == 'admin':
                Administrateur.objects.create(user=user)

            return Response(user_serializer.data, status=status.HTTP_201_CREATED)
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

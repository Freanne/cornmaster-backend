from rest_framework import serializers
from .models import CustomUser, Agriculteur, ExpertAgricole, Administrateur
from django.contrib.auth.hashers import make_password

class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_confirmation = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'username', 'email', 'numero_phone', 'role', 'password', 'password_confirmation']
    
    def validate(self, data):
        # Vérifier si les mots de passe correspondent
        if data['password'] != data['password_confirmation']:
            raise serializers.ValidationError("Les mots de passe ne correspondent pas.")
        return data

    def create(self, validated_data):
        # Retirer password_confirmation avant la création
        validated_data.pop('password_confirmation')
        # Hasher le mot de passe
        validated_data['password'] = make_password(validated_data['password'])
        # Créer l'utilisateur
        return CustomUser.objects.create(**validated_data)
    
class AgriculteurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agriculteur
        fields = ['type_ferme', 'localisation']

class ExpertAgricoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpertAgricole
        fields = ['specialisation', 'disponibilite']

from rest_framework import serializers
from .models import UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id','name','email','age']

        def validate_email(self,value):
            if '@' not in value:
                raise serializers.ValidationError("Invalid email formate")
            return value
            
        def validate_age(self,value):
            if value < 1:
                raise serializers.ValidationError("Age must be at least 1.")
            return value
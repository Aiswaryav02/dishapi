from rest_framework import serializers
from .models import Dishes
from django.contrib.auth.models import User

class DishSerializer(serializers.Serializer):
    name=serializers.CharField()
    category=serializers.CharField()
    price=serializers.IntegerField()

class DishMserial(serializers.ModelSerializer):
    class Meta:
        model=Dishes
        fields="__all__"
    def validate(self,data):
        cost=data.get("price")
        if cost<0:
            raise serializers.ValidationError
        return data
class Userserial(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['username','password','email']
    def create(self, validated_data):
        print(validated_data)
        return User.objects.create_user(**validated_data)


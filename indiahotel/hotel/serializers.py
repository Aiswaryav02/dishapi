from rest_framework import serializers
from .models import Dishes,DishRev
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
class Revserial(serializers.ModelSerializer):
    # dish=DishMserial(many=False,read_only=True)
    class Meta:
        model=DishRev
        fields=['date','rating','review']
    def create(self, validated_data):
        user=self.context.get("user")
        dish=self.context.get("dish")
        return DishRev.objects.create(user=user,dish=dish,**validated_data)


class Userserial(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['username','password','email']
    def create(self, validated_data):
        print(validated_data)
        return User.objects.create_user(**validated_data)


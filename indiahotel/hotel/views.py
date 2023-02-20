from django.shortcuts import render
from rest_framework.views import APIView,Response
from .serializers import DishSerializer,DishMserial,Userserial,Revserial
from .models import Dishes,DishRev
from rest_framework.decorators import action
from rest_framework import status
# Create your views here.
# normal sserializer
class DishView(APIView):
    def post(self,request,*args,**kwargs):
        dish=DishSerializer(data=request.data)
        if dish.is_valid():
            name=dish.validated_data.get("name")
            cat=dish.validated_data.get("category")
            prc=dish.validated_data.get("price")
            Dishes.objects.create(name=name,category=cat,price=prc)
            return Response({"msg":"ok"})
        return Response({"msg":"failed"})
    def get(self,request,*args,**kwargs):
        if "category" in request.query_params:
            cat=request.query_params.get("category")
            dishes=Dishes.objects.filter(category=cat)
            des_dish=DishSerializer(dishes,many=True)
            return Response(data=des_dish.data)
        dishes=Dishes.objects.all()
        des_dish=DishSerializer(dishes,many=True)
        return Response(data=des_dish.data)
        
class SpecificdishItem(APIView):
    def get(self,request,*args,**kwargs):
        id=kwargs.get('id')
        dish=Dishes.objects.get(id=id)
        des_dish=DishSerializer(dish)
        return Response(data=des_dish.data)
    def delete(self,request,*args,**kwargs):
        id=kwargs.get('id')
        dish=Dishes.objects.get(id=id)
        dish.delete()
        return Response({"msg":"ok"})
    def put(self,request,*args,**kwargs):
        id=kwargs.get('id')
        newdish=DishSerializer(data=request.data)
        if newdish.is_valid():
            olddish=Dishes.objects.get(id=id)
            olddish.name=newdish.validated_data.get('name')
            olddish.category=newdish.validated_data.get('category')
            olddish.price=newdish.validated_data.get('price')
            olddish.save()
            return Response({"msg":"ok"})
        return Response({"msg":"failed"})
# model serializer

class DishMView(APIView):
    def post(self,request,*args,**kwargs):
        dish=DishMserial(data=request.data)
        if dish.is_valid():
            dish.save()
            return Response({"msg":"ok"})
        return Response({"msg":dish.errors},status=status.HTTP_404_NOT_FOUND)
    def get(self,request,*args,**kwargs):
        dishes=Dishes.objects.all()
        des_dish=DishMserial(dishes,many=True)
        return Response(data=des_dish.data)
class DishMItem(APIView):
    def get(self,request,*args,**kwargs):
        id=kwargs.get('id')
        try:
            dish=Dishes.objects.get(id=id)
            des_dish=DishMserial(dish)
            return Response(data=des_dish.data)
        except:
            return Response({"msg":"failed"},status=status.HTTP_404_NOT_FOUND)

    def delete(self,request,*args,**kwargs):
        id=kwargs.get('id')
        try:
            dish=Dishes.objects.get(id=id)
            dish.delete()
            return Response({"msg":"ok"})
        except:
            return Response({"msg":"failed"},status=status.HTTP_404_NOT_FOUND)
    def put(self,request,*args,**kwargs):
        try:
            id=kwargs.get('id')
            olddish=Dishes.objects.get(id=id)
            newdish=DishMserial(data=request.data,instance=olddish)
            if newdish.is_valid():
                newdish.save()
                return Response({"msg":"ok"})
            else:
                return Response({"msg":newdish.errors},status=status.HTTP_404_NOT_FOUND)
        except:
            return Response({"msg":newdish.errors},status=status.HTTP_404_NOT_FOUND)
class UserserView(APIView):
    def post(self,request,*args,**kwargs):
        try:
            newuser=Userserial(data=request.data)
            if newuser.is_valid():
                newuser.save()
                return Response({"msg":"ok"})
            else:
                return Response({"msg":newuser.errors},status=status.HTTP_404_NOT_FOUND)
        except:
            return Response({"msg":"failed"},status=status.HTTP_404_NOT_FOUND)

# view using viewset

from rest_framework.viewsets import ViewSet,ModelViewSet
from rest_framework import permissions,authentication
class DishViewset(ViewSet):
    def create(self,request,*args,**kwargs):
        dish=DishMserial(data=request.data)
        if dish.is_valid():
            dish.save()
            return Response({"msg":"ok"})
        return Response({"msg":dish.errors},status=status.HTTP_404_NOT_FOUND)
    def list(self,request,*args,**kwargs):
        dishes=Dishes.objects.all()
        if "category" in request.query_params:
            cat=request.query_params.get("category")
            dishes=dishes.filter(category=cat)
        if "price_lt" in request.query_params:
            pl=request.query_params.get("price_lt")
            dishes=dishes.filter(price__lte=pl)
        des_dish=DishMserial(dishes,many=True)
        return Response(data=des_dish.data)
    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get('pk')
        try:
            dish=Dishes.objects.get(id=id)
            des_dish=DishMserial(dish)
            return Response(data=des_dish.data)
        except:
            return Response({"msg":"failed"},status=status.HTTP_404_NOT_FOUND)
    def update(self,request,*args,**kwargs):
        try:
            id=kwargs.get('pk')
            olddish=Dishes.objects.get(id=id)
            newdish=DishMserial(data=request.data,instance=olddish)
            if newdish.is_valid():
                newdish.save()
                return Response({"msg":"ok"})
            else:
                return Response({"msg":newdish.errors},status=status.HTTP_404_NOT_FOUND)
        except:
            return Response({"msg":newdish.errors},status=status.HTTP_404_NOT_FOUND)
    def destroy(self,request,*args,**kwargs):
        id=kwargs.get('pk')
        try:
            dish=Dishes.objects.get(id=id)
            dish.delete()
            return Response({"msg":"ok"})
        except:
            return Response({"msg":"failed"},status=status.HTTP_404_NOT_FOUND)

# views using modelviewset
class DishModViewset(ModelViewSet):
    serializer_class=DishMserial
    queryset=Dishes.objects.all()
    model=Dishes
    # authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    @action(detail=True,methods=['get']) 
    def get_review(self,request,*args,**kwargs):
        did=kwargs.get("pk")
        dish=Dishes.objects.get(id=did)
        qs=DishRev.objects.filter(dish=dish)
        ser=Revserial(qs,many=True)
        return Response(data=ser.data)  

    @action(detail=True,methods=["post"])   
    def add_review(self,request,*args,**kwargs):
        did=kwargs.get("pk")
        dish=Dishes.objects.get(id=did)
        user=request.user
        ser=Revserial(data=request.data,context={"user":user,"dish":dish})
        if ser.is_valid():
            ser.save()
            return Response(data=ser.data)
        else:
            return Response({"msg":"failed"},status=status.HTTP_404_NOT_FOUND)








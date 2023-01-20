from django.urls import path
from .views import *
urlpatterns = [
    path('dish',DishMView.as_view()),
    path('dish/<int:id>',DishMItem.as_view()),
    path('user',UserserView.as_view())
]

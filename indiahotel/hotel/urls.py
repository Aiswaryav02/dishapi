from django.urls import path
from .views import *
# from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
urlpatterns = [
    path('dish',DishMView.as_view()),
    path('dish/<int:id>',DishMItem.as_view()),
    path('user',UserserView.as_view()),
    # path('token',obtain_auth_token),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]

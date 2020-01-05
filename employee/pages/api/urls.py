"""pages/api URL Configuration

"""
# from django.conf.urls import url
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    BlogPostRUDView,
    BlogPostAPIView,
    CreateUserView,
    )

# # Create a router and register our viewsets with it.
# router = DefaultRouter()
# router.register(r'users', CreateUserView, base_name='register-user')

app_name = 'api-pages'
urlpatterns = [
    path('', BlogPostAPIView.as_view(), name='pages-listcreate'),
    path('<int:pk>/', BlogPostRUDView.as_view(), name='pages-rud'),
    # path('', include(router.urls)),
    path('register/', CreateUserView.as_view({'post': 'create'}), name='register'),
]

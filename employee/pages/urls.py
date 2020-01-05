"""pages URL Configuration

"""
from django.urls import path
from pages.views import (
    home_view,
    contact_view,
    about_view,
    pages_list_view,
    github_view,
    oxford_view,
    email_view,
    )

urlpatterns = [
    path('', home_view, name='home'),
    path('contact/', contact_view),
    path('about/', about_view),
    path('list/', pages_list_view),
    path('github/', github_view),
    path('oxford/', oxford_view),
    path('email/', email_view),
]

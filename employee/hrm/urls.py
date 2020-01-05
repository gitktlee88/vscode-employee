"""hrm URL Configuration
"""
from django.urls import path, include
from django.conf.urls import url

from hrm.api import (
    UserList,
    UserDetail,
    UserAuthentication
    )

app_name = 'hrm'

urlpatterns = [
    url(r'^users_list/$', UserList.as_view(), name='user_list'),
    url(r'^users_list/(?P<employee_id>\d+)/$', UserDetail.as_view(), name='user_list'),
    url(r'^auth/$', UserAuthentication.as_view(), name='User Authentication API'),
    # path('users_list', UserList.as_view(), name='user_list'),
    # path('users_list/int<employee_id>', UserDetail.as_view(), name='user_detail'),

]

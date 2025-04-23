from django.urls import path
from .views import (
    UserListView,
    UserCreateView,
    UserUpdateView,
    user_delete, UserDetailView,
)

urlpatterns = [
    path('',               UserListView.as_view(),   name='user-list'),
    path('create/',        UserCreateView.as_view(), name='user-create'),
    path('<int:pk>/edit/', UserUpdateView.as_view(), name='user-edit'),
    path('<int:pk>/delete/', user_delete, name='user-delete'),
    path('<int:pk>/confirm_delete/', UserDetailView.as_view(), name='user-confirm-delete'),
    path('<int:pk>/view/', UserDetailView.as_view(), name='user-view'),

]

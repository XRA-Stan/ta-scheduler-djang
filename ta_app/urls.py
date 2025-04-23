"""
URL configuration for ta_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path

from ta_scheduler import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.loginUser, name = "login"),
    path('home/', views.home, name = "home"),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('HomePageTemplate/', views.HomePageTemplate, name = 'HomePageTemplate'),

    path('home/Courses.html', views.courses, name = 'courses'),

    path('create-course/', views.course_creation_view, name='create_course'),
]

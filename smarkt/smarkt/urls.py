"""smarkt URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import include, path
from django.contrib.auth import views as auth_views

from . import views

api_patterns = [
    path('products/', include('products.urls'), name = 'products'),
    path('receipts/', include('receipts.urls'), name = 'receipts'),
]

urlpatterns = [
    path('', views.index, name='home'),
    path('login/', auth_views.login, name='login'),
    path('logout/', auth_views.logout, {'next_page': '/'} ,name='logout'),
    path('register/', views.signup, name='signup'),
	path('api/', include(api_patterns)),
    path('admin/', admin.site.urls),
    path('auth/', include('rest_framework.urls', 
        namespace='rest_framework')),
    path('o/', include('oauth2_provider.urls', 
        namespace='oauth2_provider')),
    path('accounts/', include('django.contrib.auth.urls')),
]
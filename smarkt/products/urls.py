from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import CreateView

urlpatterns = [
    path('', CreateView.as_view(), name='create_product'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
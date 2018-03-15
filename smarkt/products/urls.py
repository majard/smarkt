from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import CreateView, DetailsView

urlpatterns = [
    path('', CreateView.as_view(), name='create_product'),
    path('<pk>/', DetailsView.as_view(), name = "product_details"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
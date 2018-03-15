from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import CreateView, DetailsView

urlpatterns = [
    path('', CreateView.as_view(), name='create_receipt'),
    path('<pk>/', DetailsView.as_view(), name = "receipt_details"),
]

#Allows to automatically serve in the format requested (JSON, HTML)
urlpatterns = format_suffix_patterns(urlpatterns)
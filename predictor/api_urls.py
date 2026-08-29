from django.urls import path
from .views import predict_insurance

urlpatterns = [
    path(
        "predict/",
        predict_insurance,
        name="predict"
    ),
]
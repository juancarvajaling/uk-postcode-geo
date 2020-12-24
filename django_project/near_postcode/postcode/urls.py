from django.urls import path, include
from .views import PostcodeCreateAPIView, CoordinateCreateAPIView


urlpatterns = [
    path(
        'postcodes/',
        PostcodeCreateAPIView.as_view(),
        name='create_postcode'
    ),
    path(
        'coordinates/',
        CoordinateCreateAPIView.as_view(),
        name='create_coordinate'
    ),
]

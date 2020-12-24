from rest_framework import generics, status
from rest_framework.validators import ValidationError
from rest_framework.response import Response

from .models import Postcode, Coordinate
from .serializers import PostcodeSerializer, CoordinateSerializer


class PostcodeCreateAPIView(generics.CreateAPIView):
    
    serializer_class = PostcodeSerializer

    def create(self, request, *args, **kwargs):
        queryset = Postcode.objects.filter(code=request.data['code'])
        if queryset.exists():
            postcode = queryset.first()
            serializer = self.get_serializer(postcode)
            return Response(serializer.data, status=status.HTTP_200_OK)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class CoordinateCreateAPIView(generics.CreateAPIView):

    queryset = Coordinate.objects.all()
    serializer_class = CoordinateSerializer

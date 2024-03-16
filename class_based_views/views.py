from rest_framework.generics import (ListAPIView,
                                     ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView)
from product.models import Review
from product.serializer import ReviewSerializer
from class_based_views.serializers import UserCreateSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.views import APIView


class RegisterApiView(APIView):
    serializer_class = UserCreateSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        # username = request.data.get('username')
        # password = request.data.get('password')
        User.objects.create_user(**serializer.validated_data)
        return Response(data={'message': 'user created succesfully'},
                        status=status.HTTP_201_CREATED)

class ReviewListApiView(ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    # pagination_class = PageNumberPagination
    text = ['text']
    filterset_class = ['text', 'product']

class ReviewUpdateDeleteApiView(RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    lookup_field = 'id'


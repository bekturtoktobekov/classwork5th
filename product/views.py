from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from . import serializer, models
from rest_framework import status
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated


@api_view(['GET', 'POST'])
def product_list_view(request):
    if request.method == 'GET':
        product = models.Product.objects.all()


        data = serializer.ProductSerializer(product, many=True).data
        return Response(data=data)
    elif request.method == "POST":
        serializers = serializer.ProductCreateUpdateSerializer(data=request.data)
        if not serializers.is_valid():
            return Response(data={'errors': serializers.errors}, status=status.HTTP_406_NOT_ACCEPTABLE)
        print(request.data)
        product = models.Product.objects.create(**request.data)
        for i in request.data.get("reviews", []):
            models.Review.objects.create(stars=i['stars'], text=i['text'], product=product)
        return Response(data=serializer.ProductSerializer(product).data,
                        status=status.HTTP_201_CREATED)

@api_view(['GET', 'PUT', 'DELETE'])
def product_detail_view(request, id):
    try:
        product_id = models.Product.objects.get(id=id)
    except models.Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND, data={'message': 'Product not found'})
    if request.method == 'GET':
        data = serializer.ProductSerializer(product_id).data
        return Response(data=data)
    elif request.method == 'DELETE':
        product_id.delete()
        return Response(status=status.HTTP_204_NO_CONTENT,
                        data={'message': 'Product has been deleted!'})
    elif request.method == 'PUT':
        product_id.title = request.data['title']
        product_id.description = request.data['description']
        product_id.price = request.data['price']
        product_id.category_id = request.data['category_id']
        product_id.save()
        return Response(data=serializer.ProductSerializer(product_id).data)


@api_view(['GET'])
def test(request):
    context = {
        'integer': 100,
        'string': 'hello world',
        'boolean': True,
        'list': [
            1, 2, 3
        ]
    }
    return Response(data=context)

@api_view(['POST'])
def authorization(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            Token.objects.create(user=user).delete()
            # try:
            #     token = Token.objects.get(user=user)
            # except Token.DoesNotExist:
            #     token = Token.objects.create(user=user)
            token = Token.objects.create(user=user)
            return Response(data={'key': token.key},
                            status=status.HTTP_200_OK)
        return Response(data={'error': "User not found"},
                        status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def registration(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')
        User.objects.create_user(username=username, password=password)
        return Response(data={'message': 'User created successfully'},
                        status=status.HTTP_201_CREATED)

@permission_classes([IsAuthenticated])
@api_view(['GET'])
def user_reviews(request):
    reviews = models.Review.objects.filter(author=request.user)
    serializers = serializer.ReviewSerializer(reviews, many=True)
    return Response(data=serializers.data)
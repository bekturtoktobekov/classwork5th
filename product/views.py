from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from . import serializer, models
from  rest_framework import status



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

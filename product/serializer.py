from rest_framework import serializers
from . import models
from rest_framework.exceptions import ValidationError

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = 'id name'.split()


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Review
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    # category = CategorySerializer()
    category = serializers.SerializerMethodField()
    # reviews = ReviewSerializer(many=True)
    reviews = serializers.SerializerMethodField()
    class Meta:
        model = models.Product
        fields = 'id title price category reviews count_reviews rating'.split()
        # fields = '__all__'

    def get_category(self, product):
        try:
            return f'{product.category.id}-{product.category.name}'
        except:
            return 'No category'

    def get_reviews(self, product):
        # serializer = ReviewSerializer(product.reviews.all(), many=True)
        serializer = ReviewSerializer(models.Review.objects.filter(author__isnull=False, product=product), many=True)
        return serializer.data

class ObjectCreateSerializer(serializers.Serializer):
    name = serializers.CharField()
    is_active = serializers.BooleanField()


class ProductCreateUpdateSerializer(serializers.Serializer):
    title = serializers.CharField(min_length=2, max_length=20)
    description = serializers.CharField()
    price = serializers.FloatField()
    category_id = serializers.IntegerField() #200
    list_ = serializers.ListField(child=serializers.CharField())
    object_ = ObjectCreateSerializer()

class ReviewCreateSerializer(serializers.Serializer):
    stars = serializers.IntegerField(min_value=1, max_value=5)
    text = serializers.CharField(max_length=60)


    def validate_category_id(self, category_id):
        if models.Category.objects.filter(id=category_id).count() == 0:
            raise ValidationError(f'Category with id {category_id} does not exist')

# class ObjectCreateSerializer(serializers.Serializer):
#     name = serializers.CharField()
#     is_active = serializers.BooleanField()


    # def validate(self, attrs):
    #     id = attrs.get('id')
    #     try:
    #         models.Category.objects.get(id=id)
    #     except:
    #         raise ValidationError(f'Category with id {id} doesnt exist')
    #     return attrs


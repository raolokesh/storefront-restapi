from rest_framework import serializers
from decimal import Decimal

from store.models import Product,Collection,Review

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ["id","title","products_count"]
    
    products_count = serializers.IntegerField(read_only = True)


class ProductSerializer(serializers.ModelSerializer):  

    class Meta:
        model = Product
        fields = ["id","title","unit_price","collection_name","description",
                  "price_with_tax","inventory", "collection",]
        
    # inventory = serializers.IntegerField()
    # title = serializers.CharField(max_length = 255)
    price_with_tax = serializers.SerializerMethodField(method_name="calculate_tax")
    collection = serializers.PrimaryKeyRelatedField(
        queryset = Collection.objects.all()
    )
    collection_name = serializers.StringRelatedField()

 
    def calculate_tax(self,product: Product):
        return product.unit_price * Decimal(1.1)
    

    # def create(self,validated_data):
    #     product = Product(**validated_data)
    #     product.other = 1 # type: ignore
    #     product.save()
    #     return product
    
    # def update(self,instance,validate_data):
    #     instance.unit_price = validate_data.get("unit_price")
    #     instance.save()
    #     return instance


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        field = ["id","date","name","description",  ]
        explicit_field = ["__all__"]
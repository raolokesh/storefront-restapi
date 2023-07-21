from rest_framework import serializers
from decimal import Decimal

from store.models import Cart_Item, Customer, Product,Collection,Review,Cart

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
        fields = ["id","date","name","description",]

    def create(self, validated_data):
        product_id = self.context["product_id"] 
        return Review.objects.create(product_id = product_id, **validated_data )
    

class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id","title","unit_price"]

class CartItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer(read_only = True)
    total_price = serializers.SerializerMethodField()


    def get_total_price(self,cart_item:Cart_Item):
        return cart_item.quantity * cart_item.product.unit_price

 
    class Meta:
        model = Cart_Item
        fields = ["id","product","quantity","total_price"]

class  CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only = True )
    items = CartItemSerializer(many = True,read_only = True)
    total_price = serializers.SerializerMethodField()

    def get_total_price(self,cart:Cart):
        return sum( [item.quantity * item.product.unit_price for item in cart.items.all()]) # type: ignore

    class Meta:
        model = Cart 
        fields = ["id","items","total_price"]

 
class AddCartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()

    def validate_product_id(self,value):
        if not Product.objects.filter(pk = value).exists():
            raise serializers.ValidationError("No Product with given id found")
        return value

    def save(self, **kwargs):
        cart_id = self.context["cart_id"]
        product_id = self.validated_data["product_id"] # type: ignore
        quantity = self.validated_data['quantity'] # type: ignore
        try:
            cart_item = Cart_Item.objects.get(cart_id = cart_id,product_id=product_id)
            cart_item.quantity += quantity
            cart_item.save()
            self.instance =cart_item
        except Cart_Item.DoesNotExist:
            self.instance = Cart_Item.objects.create(cart_id=cart_id,**self.validated_data) # type: ignore

        return self.instance


    class Meta:
        model = Cart_Item
        fields = ["id","product_id","quantity"]

class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart_Item
        fields = ["quantity"]


class CustomerSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only = True)
    class Meta:
        model = Customer
        fields = ['id','user_id','phone','birth_date','membership']
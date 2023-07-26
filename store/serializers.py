from rest_framework import serializers
from decimal import Decimal
from django.db import transaction
from store.signals import order_created

from store.models import Cart_Item, Customer, Order, Order_Item, Product,Collection, ProductImage,Review,Cart

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ["id","title","products_count"]
    
    products_count = serializers.IntegerField(read_only = True)


class ProductImageSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        product_id = self.context["product_id"]
        return ProductImage.objects.create(product_id=product_id,**validated_data)
    class Meta:
        model = ProductImage
        fields = ["id","image"]



class ProductSerializer(serializers.ModelSerializer):  
    images = ProductImageSerializer(many = True,read_only = True)
    class Meta:
        model = Product
        fields = ["id","title","unit_price","collection_name","description",
                  "price_with_tax","inventory", "collection","images"]
        
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


class OrderItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer(read_only = True)
    class Meta:
        model = Order_Item
        fields = ["id","product","unit_price","quantity"]

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many = True)
    class Meta:
        model = Order 
        fields = ["id","customer","placed_at",'payment_status',"items"]

class UpdateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["payment_status"]

class CreateOrderSerializer(serializers.Serializer):
    cart_id = serializers.UUIDField()

    def validate_cart_id(self, cart_id):
        if not Cart.objects.filter(pk = cart_id).exists():
            raise serializers.ValidationError("no cart with the give cart id")
        elif Cart_Item.objects.filter(cart_id = cart_id).count() == 0:
            raise serializers.ValidationError("the cart is empty")
        return cart_id

    def save(self, **kwargs):
        with transaction.atomic():
            cart_id = self.validated_data["cart_id"]
            print(self.validated_data['cart_id']) # type: ignore
            print(self.context["user_id"]) 

            customer = Customer.objects.get(user_id = self.context["user_id"])
            order = Order.objects.create(customer = customer)


            cart_items = Cart_Item.objects.filter(cart_id = cart_id)
            order_item = [
                Order_Item(
                    order = order,
                    product = item.product,
                    unit_price = item.product.unit_price,
                    quantity = item.quantity
                )  for item in cart_items]
            
            Order_Item.objects.bulk_create(order_item)

            order_created.send_robust(self.__class__,order = order)

            Cart.objects.filter(pk = cart_id).delete()




from django.db import models
from uuid import uuid4
from django.core.validators import MinValueValidator
from django.conf import settings
from django.contrib import admin

# Create your models here.
class Promotion(models.Model):
    description = models.CharField(max_length=255)
    discount = models.FloatField()

class Collection(models.Model):
    title = models.CharField(max_length=255)
    featured_product = models.ForeignKey("Product",on_delete=models.SET_NULL,null=True, related_name="+")

    def __str__(self) ->str:
        return f"{self.title}  {self.featured_product}"

    class Meta:
        ordering = ["title"]

class Product(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(null=True)
    description = models.TextField(null=True)
    unit_price = models.DecimalField(max_digits=6,decimal_places=2)
    inventory = models.IntegerField(null=True)
    last_update = models.DateTimeField(auto_now=True)
    collection = models.ForeignKey(Collection,on_delete=models.PROTECT,related_name="products")
    promotions = models.ManyToManyField(Promotion,)

    def __str__(self) -> str:
        return f"{self.title} {self.inventory}"
    
    class Meta:
        ordering = ["title"]

class Customer(models.Model):
    MEMEBERSHIP_BRONZE = "B"
    MEMEBERSHIP_SILVER = "S"
    MEMEBERSHIP_GOLD = "G"
    MEMBERSHIP_CHOICE = [
        (MEMEBERSHIP_BRONZE,'Bronze'),
        (MEMEBERSHIP_SILVER,'Silver'),
        (MEMEBERSHIP_GOLD,"Gold")
    ]
    # first_name = models.CharField(max_length=255)
    # last_name = models.CharField(max_length=255)
    # email = models.EmailField(unique=True)
    phone = models.CharField(max_length=255)
    birth_date = models.DateField(null=True)
    membership = models.CharField(max_length=1,choices=MEMBERSHIP_CHOICE,default=MEMEBERSHIP_BRONZE)
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
     
    def __str__(self) -> str:
        return f"{self.user.first_name} {self.user.last_name} {self.user.email} {self.membership}"

    @admin.display(ordering = "user__first_name")
    def first_name(self):
        return self.user.first_name
    @admin.display(ordering = "user__first_name")
    def last_name(self):
        return self.user.last_name
    
    def email(self):
        return self.user.email
    
    class Meta:
        permissions = [
            {"view_history","can_view_history"}
        ]
    

class Order(models.Model):
    PAYMENT_PENDING = "P"
    PAYMENT_COMPLETE = "C"
    PAYMENT_FAILED = 'F'

    PAYMENT_STATUS_CHOICE = [
        (PAYMENT_COMPLETE,"Complete"),
        (PAYMENT_PENDING,"Pending"),
        (PAYMENT_FAILED,"Failed")
    ]

    payment_status = models.CharField(max_length=1,choices=PAYMENT_STATUS_CHOICE,default=PAYMENT_PENDING)
    placed_at = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(Customer,on_delete=models.PROTECT,related_name= "order")
 
    def __str__(self) -> str:
        return f"{self.customer.email} {self.placed_at} {self.payment_status}"
    
    class Meta:
        ordering = ["placed_at"]
        permissions = [
            ("cancel_order",'can cancel order')
        ]
class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    # customer = models.OneToOneField(Customer,on_delete=models.CASCADE,primary_key=True)
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE) #  one to many relations
    state = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    pincode = models.CharField(max_length=10)

class Cart(models.Model):
    id = models.UUIDField(primary_key=True ,default= uuid4)
    created_at = models.DateTimeField(auto_now_add=True)

class Cart_Item(models.Model):
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE,related_name="items")
    product = models.ForeignKey(Product , on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)]
    )

    class Meta:
        unique_together = [["cart","product"]]

    def __str__(self) -> str:
        return f"{self.product}  {self.quantity}"


class Order_Item(models.Model):
    product = models.ForeignKey(Product , on_delete=models.PROTECT,related_name="orderitem")
    order = models.ForeignKey(Order,on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=8,decimal_places=2)


class Review(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name="reviews")
    name = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField(auto_now_add=True)
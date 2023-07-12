from django.db import models

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
    slug = models.SlugField()
    description = models.TextField()
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
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=255)
    birth_date = models.DateField(null=True)
    membership = models.CharField(max_length=1,choices=MEMBERSHIP_CHOICE,default=MEMEBERSHIP_BRONZE)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name} {self.email} {self.membership}"


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
    customer = models.ForeignKey(Customer,on_delete=models.PROTECT)

    def __str__(self) -> str:
        return f"{self.customer.email} {self.placed_at} {self.payment_status}"
    
    class Meta:
        ordering = ["placed_at"]

class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    # customer = models.OneToOneField(Customer,on_delete=models.CASCADE,primary_key=True)
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE) #  one to many relations
    state = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    pincode = models.CharField(max_length=10)

class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

class Cart_Item(models.Model):
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE)
    product = models.ForeignKey(Product , on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()

    def __str__(self) -> str:
        return f"{self.product}  {self.quantity}"


class Order_Item(models.Model):
    product = models.ForeignKey(Product , on_delete=models.PROTECT,related_name="orderitem")
    order = models.ForeignKey(Order,on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=8,decimal_places=2)
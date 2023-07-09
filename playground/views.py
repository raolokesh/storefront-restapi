from django.shortcuts import render
from django.db.models import Q
from store.models import Product,Order


# Create your views here.


def say_hello(request):
    
    # product = Product.objects.filter(Q(unit_price__gte = 20) & Q(unit_price__lt = 30)  )
    # order = Order_Item.objects.all().order_by("id")[:5]
    order = Order.objects.select_related("customer").order_by("-placed_at")[:5]
    return render(request,"hello.html",{
        "products":order,
    }) 
from django.shortcuts import render
from django.db.models import Q
from playground.tasks import notify_customer
from store.models import Product,Order
from django.core.mail import send_mail,mail_admins,BadHeaderError,EmailMessage
from templated_mail.mail import BaseEmailMessage

# # Create your views here.


# def say_hello(request):
    
#     # product = Product.objects.filter(Q(unit_price__gte = 20) & Q(unit_price__lt = 30)  )
#     # order = Order_Item.objects.all().order_by("id")[:5]
#     order = Order.objects.select_related("customer").order_by("-placed_at")[:5]
#     return render(request,"hello.html",{
#         "products":order,
#     }) 

# from .tasks import notify_customer

# def say_hello(request):
#     notify_customer.delay("hello")
#     order = Order.objects.select_related("customer").order_by("-placed_at")[:5]
#     return render(request,"hello.html",{
#         "products":order,})


# def say_hello(request):
#     try:
        # send_mail('subject','message','info@lokesh.com',["bob@lokesh.com",'lsok@lokesh.com'])
        # mail_admins('subject','message',html_message="message")
        # message = EmailMessage('subject','message','from@lokesh.com',['john@lokesh.com'])
        # message.attach_file('playground/static/images/img1.jpg')
        # message.send()
    #     message = BaseEmailMessage(
    #         template_name='emails/hello.html',
    #         context={'name':'Lokesh'}

    #     )
    #     message.send(['john@lokesh.com'])
    #     print('mail send')
    # except BadHeaderError:
    #     pass
    # order = Order.objects.select_related("customer").order_by("-placed_at")[:5]
    # return render(request,"hello.html",{
    #     "products":order,})

    
def say_hello(request):
    notify_customer.delay("hello")
    order = Order.objects.select_related("customer").order_by("-placed_at")[:5]
    return render(request,"hello.html",{
        "products":order,})

# celery and flower for the view or observations
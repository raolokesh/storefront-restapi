from django.shortcuts import get_object_or_404
# from django.http import HttpResponse
from django.db.models.aggregates import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter,OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from rest_framework.mixins import CreateModelMixin,RetrieveModelMixin,DestroyModelMixin
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet,GenericViewSet


from store.filters import ProductFilter

from .models import Cart, Cart_Item, Product, Collection,Order_Item,Review
from .serializers import AddCartItemSerializer, CartItemSerializer, ProductSerializer, CollectionSerializer,ReviewSerializer,CartSerializer, UpdateCartItemSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend,SearchFilter,OrderingFilter]
    # filterset_fields = ["collection_id",]
    filterset_class = ProductFilter
    # pagination_class = PageNumberPagination
    search_fields = ["title","description"]
    ordering_fields = ["unit_price","last_update"]

    # def get_queryset(self):
    #     queryset = Product.objects.all()
    #     collection_id = self.request.query_params.get("collection_id")  
    #     if collection_id is not None:
    #         queryset = queryset.filter(collection_id = collection_id)
    #     return queryset
    

    def get_serializer_context(self):
        return {'request': self.request}
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.orderitem.count()>0:
            return Response({"error": "product can't delete"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)
    # def delete(self, request, pk):
    #     product = get_object_or_404(Product, pk = pk )
    #     if product.orderitem.count() > 0:  # type: ignore
    #         return Response({"error": "product can't delete"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    #     product.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)


# class ProductList(ListCreateAPIView):
#     queryset = Product.objects.select_related("collection").all()
#     serializer_class = ProductSerializer 
    # def get_queryset(self):
    #     return Product.objects.select_related("collection").all()

    # def get_serializer_class(self):
    #      return ProductSerializer

    # def get_serializer_context(self):
    #     return {'request': self.request}


# class ProductList(APIView):
#      def get(self,request):
#         product = Product.objects.select_related("collection").all()
#         serializer = ProductSerializer(product,  many = True)
#         # return HttpResponse("product")
#         return Response(serializer.data)
#      def post(self,request):
#         serializer = ProductSerializer(data = request.data )
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         serializer.validated_data
#         return Response(serializer.data,status=status.HTTP_201_CREATED)

# @api_view(["GET",'POST'])
# def product_list(request):
#     if request.method == "GET":
#         product = Product.objects.select_related("collection").all()
#         serializer = ProductSerializer(product,  many = True)
#         # return HttpResponse("product")
#         return Response(serializer.data)
#     elif request.method == "POST":
#         serializer = ProductSerializer(data = request.data )
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         serializer.validated_data
#         return Response(serializer.data,status=status.HTTP_201_CREATED)
#         # if serializer.is_valid() :
#         #     serializer.validated_data
#         #     return Response("ok")
#         # else:
#         #      return Response(serializer.errors,status=status.HTTP_404_NOT_FOUND)
# class ProductDetail(RetrieveUpdateDestroyAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     # lookup_field = id
#     def delete(self, request, pk):
#         product = get_object_or_404(Product, pk = pk )
#         if product.orderitem.count() > 0:  # type: ignore
#             return Response({"error": "product can't delete"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# class ProductDetail(APIView):
#     #  product = get_object_or_404(Product,pk = id)
#     def get(self, request, id):
#         product = get_object_or_404(Product, pk=id)
#         serializer = ProductSerializer(product)
#         return Response(serializer.data)

#     def put(self, request, id):
#         serializer = ProductSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     def delete(self, request, id):
#         product = get_object_or_404(Product, pk=id)
#         if product.orderitem.count() > 0:  # type: ignore
#             return Response({"error": "product can't delete"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# @api_view(["GET","PUT","DELETE"])
# def product_detail(request,id):
#         product = get_object_or_404(Product,pk = id)
#         if request.method == "GET":
#             serializer = ProductSerializer(product)
#             return Response(serializer.data)
#         elif request.method == "PUT":
#              serializer = ProductSerializer(data = request.data)
#              serializer.is_valid(raise_exception=True)
#              serializer.save()
#              return Response(serializer.data,status=status.HTTP_200_OK)
#         elif request.method == "DELETE":
#             # if product.order_item__get.count()>0:
#             #     return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
#             #  serializer = ProductSerializer(data= reques t.data)
#             product.delete()
#             return Response(status=status.HTTP_204_NO_CONTENT)
#     # try:
#     #     product = Product.objects.get(pk = id)
#     #     serializer = ProductSerializer(product)
#     #     return Response(serializer.data)
#     # except Product.DoesNotExist:
#     #     # return Response(status=404)
#     #     return Response(status=status.HTTP_404_NOT_FOUND)


class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(products_count = Count("products")).all()
    serializer_class = CollectionSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.products.count() > 0:  # type: ignore
            return Response({"error"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)

    # def delete(self, request, pk ):
    #     collection = get_object_or_404(Collection.objects.annotate( 
    #         products_count=Count("products")), pk = pk )
    #     if collection.products.count() > 0:  # type: ignore
    #         return Response({"error"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    #     collection.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)

# class CollectionList(ListCreateAPIView): 
#     queryset = Collection.objects.annotate(
#         products_count=Count("products")).all()
#     serializer_class = CollectionSerializer


# @api_view(["GET","POST"])
# def collection_list(request):
#     if request.method == "GET":
#         queryset = Collection.objects.annotate(products_count = Count("products")).all()
#         serializer = CollectionSerializer(queryset, many = True)
#         return Response(serializer.data)

#     elif request.method == "POST":
#         serializer = ProductSerializer(data = request.data )
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         serializer.validated_data
#         return Response(serializer.data,status=status.HTTP_201_CREATED)




# class CollectionDetail(RetrieveUpdateDestroyAPIView):
#     queryset = Collection.objects.annotate( products_count=Count("products")).all()
#     serializer_class = CollectionSerializer
#     def delete(self, request, pk ):
#         collection = get_object_or_404(Collection.objects.annotate( 
#             products_count=Count("products")), pk = pk )
#         if collection.products.count() > 0:  # type: ignore
#             return Response({"error"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         collection.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# class CollectionDetail(APIView):
#     def get(self, request, pk):
#         collection = get_object_or_404(Collection.objects.annotate(
#             products_count=Count("products")), pk=pk)
#         serializer = CollectionSerializer(collection)
#         return Response(serializer.data)

    # def put(self, request, pk):
    #     serializer = CollectionSerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializer.data, status=status.HTTP_200_OK)

    # def delete(self, request, pk):
    #     collection = get_object_or_404(Collection.objects.annotate(
    #         products_count=Count("products")), pk=pk)
    #     if collection.products.count() > 0:  # type: ignore
    #         return Response({"error"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    #     collection.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)

# @api_view(["GET","PUT","DELETE"])
# def collection_detail(request,pk):
#         collection = get_object_or_404(Collection.objects.annotate(products_count = Count("products")),pk = pk )
#         if request.method == "GET":
#             serializer = CollectionSerializer(collection)
#             return Response(serializer.data)
#         elif request.method == "PUT":
#              serializer = CollectionSerializer(data = request.data)
#              serializer.is_valid(raise_exception=True)
#              serializer.save()
#              return Response(serializer.data,status=status.HTTP_200_OK)
#         elif request.method == "DELETE":
#             if collection.products.count()> 0: # type: ignore
#                 return Response({"error"},status=status.HTTP_405_METHOD_NOT_ALLOWED)
#             collection.delete()
#             return Response(status=status.HTTP_204_NO_CONTENT)




class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(product_id = self.kwargs["product_pk"])

    def get_serializer_context(self):
        return {"product_id":self.kwargs["product_pk"]}
    




class CartViewSet(CreateModelMixin,GenericViewSet,RetrieveModelMixin,DestroyModelMixin):
    queryset = Cart.objects.prefetch_related("items","items__product").all()
    serializer_class = CartSerializer
    

class CartItemViewSet(ModelViewSet):
    http_method_names = ["get","delete","post","patch"]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return AddCartItemSerializer
        elif self.request.method == "PATCH":
            return UpdateCartItemSerializer
        return CartItemSerializer
    
    def get_serializer_context(self):
        return {"cart_id": self.kwargs["cart_pk"]}

    def get_queryset(self):
        return Cart_Item.objects.filter(cart_id = self.kwargs['cart_pk']).select_related("product")
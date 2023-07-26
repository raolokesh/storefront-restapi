from django.urls import path,include
from rest_framework.routers import SimpleRouter,DefaultRouter
from rest_framework_nested import routers
from rest_framework.urlpatterns import format_suffix_patterns
from . import views
from pprint import pprint

router = routers.DefaultRouter()
router.register("products",views.ProductViewSet,basename="products")
router.register("collection",views.CollectionViewSet)
router.register("carts",views.CartViewSet)
router.register("customers",views.CustomerViewSet) 
router.register("order",views.OrderViewSet, basename="orders")

products_router = routers.NestedDefaultRouter(router,"products",lookup = "product")
products_router.register("reviews",views.ReviewViewSet,basename="product-reviews")
products_router.register("images",views.ProductImageViewSet,basename='product-images')

cart_router = routers.NestedDefaultRouter(router,"carts",lookup = "cart")
cart_router.register("items",views.CartItemViewSet,basename = "cart-items")
# urlpatterns = router.urls+products_router.urls


urlpatterns = [ 
    path(r"",include(router.urls)),
    path(r"",include(products_router.urls)),
    path(r"",include(cart_router.urls)),

]
 


# urlpatterns = [
#     # path("product/",views.ProductList.as_view()),
#     # path("product/<int:pk>",views.ProductDetail.as_view()),
#     # path("collection/",views.CollectionList.as_view()),
#     # path("collection/<int:pk>",views.CollectionDetail.as_view())
# ]

from django.urls import path,include
from rest_framework.routers import SimpleRouter,DefaultRouter
from rest_framework_nested import routers
from . import views
from pprint import pprint

router = routers.DefaultRouter()
router.register("product",views.ProductViewSet)
router.register("collection",views.CollectionViewSet)

products_router = routers.NestedDefaultRouter(router,"product",lookup = "product")
products_router.register("reviews",views.ReviewViewSet,basename="product-reviews-details")
# urlpatterns = router.urls+products_router.urls


urlpatterns = [ 
    path("",include(router.urls)),
    path("",include(products_router.urls)),

]


# urlpatterns = [
#     # path("product/",views.ProductList.as_view()),
#     # path("product/<int:pk>",views.ProductDetail.as_view()),
#     # path("collection/",views.CollectionList.as_view()),
#     # path("collection/<int:pk>",views.CollectionDetail.as_view())
# ]

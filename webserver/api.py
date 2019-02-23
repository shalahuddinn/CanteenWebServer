from rest_framework import routers
from . import api_views

router = routers.DefaultRouter()
router.register(r'order', api_views.OrderViewset)
router.register(r'seller', api_views.SellerViewset)
router.register(r'menu', api_views.MenuViewset)
router.register(r'detailorder', api_views.OrderDetailViewset)
# router.register(r'queue', api_views.QueueTransactionViewset)
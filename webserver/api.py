from rest_framework import routers
from . import api_views

router = routers.DefaultRouter()
router.register(r'order', api_views.OrderViewset)
router.register(r'seller', api_views.SellerViewset, base_name='Seller')
router.register(r'menu', api_views.MenuViewset)
router.register(r'orderdetail', api_views.OrderDetailViewset, base_name='OrderDetail')
router.register(r'payment', api_views.PaymentViewset)
# router.register(r'queue', api_views.QueueTransactionViewset)

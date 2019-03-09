from rest_framework import viewsets
from . import models
from . import serializers

class OrderViewset(viewsets.ModelViewSet):
    queryset = models.Order.objects.all()
    serializer_class = serializers.OrderSerializer

class SellerViewset(viewsets.ModelViewSet):
    # queryset = models.Seller.objects.all()
    serializer_class = serializers.SellerSerializer

    def get_queryset(self):
        queryset = models.Seller.objects.all()
        username = self.request.query_params.get('username', None)
        if username is not None:
            queryset = queryset.filter(username=username)
        return queryset

class MenuViewset(viewsets.ModelViewSet):
    queryset = models.Menu.objects.all()
    serializer_class = serializers.MenuSerializer

    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)
    #     headers = self.get_success_headers(serializer.data)
    #     last_obj = models.Menu.objects.last()
    #     return Response({str(last_obj)}, status=status.HTTP_201_CREATED, headers=headers)


class OrderDetailViewset(viewsets.ModelViewSet):
    queryset = models.OrderDetail.objects.all()
    serializer_class = serializers.OrderDetailSerializer

# class OrderedMenuViewSet(viewsets.ViewSet):
#     serializer_class = serializers.OrderedMenuSerializer
#     queryset = models.OrderDetail.objects.all()
    # def list(self, request):
    #     orderedmenu = Orderedmenu(menu=models.Menu.objects.all(), order=models.OrderDetail.objects.all())
    #     serializer_class = serializers.OrderedMenuSerializer(orderedmenu, context={"request": request})
    #     return Response(serializer_class.data)

# class QueueTransactionViewset(viewsets.ModelViewSet):
#     queryset = models.QueueTransaction.objects.all()
#     serializer_class = serializers.QueueTransactionSerializer
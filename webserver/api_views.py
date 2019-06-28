from rest_framework import viewsets, status
from rest_framework.response import Response

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

    def get_queryset(self):
        queryset = models.Menu.objects.all()
        sellerID = self.request.query_params.get('sellerID', None)
        if sellerID is not None:
            queryset = queryset.filter(sellerID=sellerID)
        return queryset

    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)
    #     headers = self.get_success_headers(serializer.data)
    #     last_obj = models.Menu.objects.last()
    #     return Response({str(last_obj)}, status=status.HTTP_201_CREATED, headers=headers)


class OrderDetailViewset(viewsets.ModelViewSet):
    serializer_class = serializers.OrderDetailSerializer
    def get_queryset(self):
        queryset = models.OrderDetail.objects.all()
        sellerID = self.request.query_params.get('sellerID', None)
        itemStatus = self.request.query_params.get('itemStatus', None)
        if sellerID is not None:
            queryset = queryset.filter(sellerID=sellerID)
            if itemStatus is not None:
                queryset = queryset.filter(sellerID=sellerID, itemStatus=itemStatus)
        return queryset

    # Enable Post of List
    # https://stackoverflow.com/questions/37329771/django-rest-bulk-post-post-array-of-json-objects
    # Accessed on March 9, 2019
    def create(self, request, pk=None, company_pk=None, project_pk=None):
        is_many = True if isinstance(request.data, list) else False
        print("Is_many:")
        print(is_many)

        serializer = self.get_serializer(data=request.data, many=is_many)
        serializer.is_valid(raise_exception=True)

        # valid = serializer.is_valid()
        # print("valid: {}".format(valid))
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class PaymentViewset(viewsets.ModelViewSet):
    queryset = models.Payment.objects.all()
    serializer_class = serializers.PaymentSerializer


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

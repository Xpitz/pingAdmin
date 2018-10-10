from .serializers import AssetInfoSerializer, AssetGroupSerializer
from .models import AssetInfo, AssetGroup
from rest_framework import viewsets


class AssetViewSet(viewsets.ModelViewSet):
    queryset = AssetInfo.objects.all()
    serializer_class = AssetInfoSerializer


class AssetGroupViewSet(viewsets.ModelViewSet):
    queryset = AssetGroup.objects.all()
    serializer_class = AssetGroupSerializer

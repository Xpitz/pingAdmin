from rest_framework import serializers
from .models import AssetInfo, AssetGroup


class AssetInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetInfo
        fields = '__all__'


class AssetGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetGroup
        fields = '__all__'

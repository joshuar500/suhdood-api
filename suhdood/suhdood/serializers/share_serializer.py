from rest_framework import serializers
from suhdood.models.share import Share
from suhdood.serializers.url_serializer import UrlSerializer

class ShareSerializer(serializers.HyperlinkedModelSerializer):
    shared_url = UrlSerializer()
    class Meta:
        model = Share
        fields = ('sender', 'receiver', 'shared_url', 'date', 'viewed')

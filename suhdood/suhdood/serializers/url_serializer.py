from rest_framework import serializers
from suhdood.models.url import Url

class UrlSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Url
        fields = ('url_string',)

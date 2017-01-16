from rest_framework import serializers
from suhdood.models.share import Share

class ShareSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Share
        fields = ('sender', 'receiver', 'shared_url', 'date')

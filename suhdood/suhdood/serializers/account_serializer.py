from rest_framework import serializers
from suhdood.models.account import Account
from friendship.models import Friend, Follow, FriendshipRequest

class AccountSerializer(serializers.Serializer):
    email = serializers.EmailField(read_only=True)
    display_name = serializers.CharField(max_length=255)

    def create(self, validated_data):
        return Account.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.display_name = validated_data.get('display_name', instance.display_name)

    class Meta:
        model = Account
        fields = ('email', 'display_name',)

class FriendshipRequestReadSerializer(serializers.ModelSerializer):
    from_user = AccountSerializer()
    to_user = AccountSerializer()
    created_at = serializers.DateTimeField(source='created')

    class Meta:
        model = FriendshipRequest
        exclude = ('message', 'viewed', 'rejected', 'created',)

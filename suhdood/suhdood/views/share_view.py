from rest_framework import viewsets
from suhdood.serializers.share_serializer import ShareSerializer
from suhdood.models.share import Share
from suhdood.models.url import Url
from rest_framework.decorators import api_view
from rest_framework.response import Response
from friendship.models import Friend
from suhdood.models.account import Account

class ShareViewSet(viewsets.ModelViewSet):
    queryset = Share.objects.all().order_by('date')
    serializer_class = ShareSerializer

@api_view(['GET'])
def received_shares(request):
    # get logged in users' shares from friends
    uid = request.user.id
    if request.method == 'GET':
        shares = Share.objects.filter(receiver=uid).all()
        serialized_shares = ShareSerializer(shares, context={'request': request}, many=True)
        return Response(serialized_shares.data)

@api_view(['GET', 'POST'])
def sent_shares(request):
    if request.method == 'GET':
        shares = Share.objects.filter(receiver="49d119e5-f7b5-474b-83f2-dbf7973bad9c").all()
        serialized_shares = ShareSerializer(shares, context={'request': request}, many=True)
        return Response(serialized_shares.data)

@api_view(['GET', 'POST'])
def share(request):
    if request.method == 'POST':
        from_user = request.user
        to_user_id = request.data['to_user_id']
        url_string = request.data['url_string']

        to_user_account = Account.objects.filter(id=to_user_id).first()

        if Friend.objects.are_friends(request.user, to_user_account):
            print('we friends!')
            created_url = Url.objects.create_url(url_string)
            created_share = Share.objects.create(
                sender=request.user,
                receiver=to_user_account,
                shared_url=created_url
                )
        return Response(status=204)
    return Response()
        
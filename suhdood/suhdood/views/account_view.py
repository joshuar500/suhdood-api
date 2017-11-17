from suhdood.serializers.account_serializer import AccountSerializer, FriendshipRequestReadSerializer
from suhdood.models.account import Account
from rest_framework import serializers, viewsets, mixins
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view
from friendship.models import Friend, Follow, FriendshipRequest

class AccountViewSet(viewsets.ModelViewSet, mixins.ListModelMixin):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated]

@api_view(['GET', 'POST'])
def sign_up(request):
    if request.method == 'POST':
        email = request.data['email']
        display_name = request.data['display_name']
        password = request.data['password']

        # does account already exist?
        account = Account.objects.filter(email=email).first()

        if account:
            print('Account already exists')
            return Response(status=499)
        else:
            Account.objects.create_user(
                email = email,
                display_name = display_name,
                password=password
            )

        return Response(status=200)
    return Response()

@api_view(['GET'])
def get_user_friends(request, display_name):
    if request.method == 'GET':
        account = Account.objects.filter(display_name=display_name).first()
        friends_list = Friend.objects.friends(account)
        print(friends_list)
        friends_list_serializer = AccountSerializer(friends_list, context={'request': request}, many=True)
        print(friends_list_serializer.data)
        return Response(friends_list_serializer.data)

@api_view(['GET', 'POST'])
def add_friend(request):
    if request.method == 'POST':
        other_user = request.data['other_user']
        message = request.data['message']
        print(other_user)
        print(message)
        other_user_account = Account.objects.filter(email=other_user).first()
        Friend.objects.add_friend(
            request.user,
            other_user_account,
            message=message
        )
        return Response(status=200)
    return Response()

@api_view(['GET'])
def unread_requests(request):
    if request.method == 'GET':
        unread_requests = Friend.objects.unread_requests(user=request.user)
        print(unread_requests)
        unread_requests_serializer = FriendshipRequestReadSerializer(unread_requests, context={'request': request}, many=True)
        print(unread_requests_serializer)
        return Response(unread_requests_serializer.data, status=204)

@api_view(['GET', 'POST'])
def accept_request(request):
    if request.method == 'POST':
        friend_request_id = request.data['request_id']
        friend_request = FriendshipRequest.objects.get(id=friend_request_id)
        friend_request.accept()
        return Response(status=200)
    return Response()
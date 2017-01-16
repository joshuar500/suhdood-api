from django.conf.urls import url, include
from django.contrib import admin
from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token
from suhdood.views import share_view, account_view

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'accounts', account_view.AccountViewSet)
router.register(r'shares', share_view.ShareViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^admin/', admin.site.urls),
    url(r'^friendship/', include('friendship.urls')),
    url(r'^(?P<display_name>.+)/friends/$', account_view.get_user_friends),
    url(r'^add_friend/$', account_view.add_friend),
    url(r'^accept_request/$', account_view.accept_request),
    url(r'^unread_requests/$', account_view.unread_requests),
    url(r'^received_shares/$', share_view.received_shares),
    url(r'^sent_shares/$', share_view.received_shares),
    url(r'^share/$', share_view.share),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^login/', obtain_jwt_token)
]

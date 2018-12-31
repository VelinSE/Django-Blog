from django.conf.urls import url, include

from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

#from rest.views import UserViewSet, UsersView, UserDetails, posts_list, post_details
#from rest.views import PostsList, PostDetails, UsersList, UserDetails, 
from rest.views import UserViewSet, PostViewSet, api_root

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'posts', PostViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^auth/', include('rest_framework.urls')),
    # url(r'^posts/$', PostsList.as_view(), name="Posts"),
    # url(r'^posts/(?P<pk>\d+)/$', PostDetails.as_view(), name="PostDetails"),
    # url(r'^users/$', UsersList.as_view(), name="Users"),
    # url(r'^users/(?P<pk>\d+)/$', UserDetails.as_view(), name="UserDetails")
]

#urlpatterns = format_suffix_patterns(urlpatterns)
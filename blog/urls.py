from django.conf.urls import url

from blog.views import create, display_post, delete_post, display_all_posts, update_post

urlpatterns = [
    url(r'^posts/$', display_all_posts, name="DisplayPosts"),
    url(r'^posts/create/$', create, name="CreatePost"),
    url(r'^post/delete/$', delete_post, name="DeletePost"),
    url(r'^post/(?P<post_id>\d+)/$', display_post, name="DisplayPost"),
    url(r'^post/(?P<post_id>\d+)/update/$', update_post, name="DisplayPost")
]

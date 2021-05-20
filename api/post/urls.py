from django.urls    import path

from api.post.views     import PostListGenericsAPIView

app_name='post'

urlpatterns = [
    path('/', PostListGenericsAPIView.as_view(), name='post-list'),
]

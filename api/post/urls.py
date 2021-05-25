from django.urls    import path

from api.post.views     import PostCreateGenericsAPIView, PostDetailGenericsAPIView, PostListGenericsAPIView

app_name='post'

urlpatterns = [
    path('/', PostListGenericsAPIView.as_view(), name='post-list'),
    path('/<int:pk>', PostDetailGenericsAPIView.as_view(), name='post-detail'),
    path('/create', PostCreateGenericsAPIView.as_view(), name='post-create')
]

from rest_framework             import generics, status
from rest_framework.response    import Response
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly

from user.models    import Address, Filter, User
from post.models    import Post
from .serializers   import PostDetailSerializer, PostListSerializer

class PostListGenericsAPIView(generics.ListAPIView):
    serializer_class    = PostListSerializer
    permission_classes  = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        address = Address.objects.get(user_id=self.request.user.id, is_main=True)
        
        exclude_filters         = Filter.objects.filter(user_id=self.request.user.id, is_active=False)
        excluded_subcategories  = [exclude_filter.subcategory_id for exclude_filter in exclude_filters]

        posts   = Post.objects.filter(address=address.name).exclude(subcategory_id__in = excluded_subcategories)

        return posts

class PostDetailGenericsAPIView(generics.RetrieveAPIView):
    queryset            = Post.objects.all()
    serializer_class    = PostDetailSerializer
    permission_classes  = [IsAuthenticatedOrReadOnly]

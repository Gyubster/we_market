from rest_framework             import generics, status
from rest_framework.response    import Response
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly

from user.models    import Address, Filter, User
from post.models    import Post, Subcategory, PostImage, Status
from .serializers   import PostSerializer, PostDetailSerializer, PostListSerializer

class PostListGenericsAPIView(generics.ListAPIView):
    serializer_class    = PostListSerializer
    permission_classes  = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        address = Address.objects.get(user_id=self.request.user.id, is_main=True)
        
        exclude_filters         = Filter.objects.filter(user_id=self.request.user.id, is_active=False)
        excluded_subcategories  = [exclude_filter.subcategory_id for exclude_filter in exclude_filters]

        posts   = Post.objects.filter(address=address.name).exclude(subcategory_id__in = excluded_subcategories)

        return posts

class PostDetailGenericsAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset            = Post.objects.all()
    serializer_class    = PostDetailSerializer
    permission_classes  = [IsAuthenticatedOrReadOnly]

class PostCreateGenericsAPIView(generics.CreateAPIView):
    queryset            = Post.objects.all()
    serializer_class    = PostSerializer
    permission_classes  = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            post = Post.objects.create(
                    user_id             = request.user.id,
                    subcategory_id      = request.data['subcategory'],
                    status_id           = request.data['status'],
                    product             = request.data['product'],
                    address             = Address.objects.get(user_id=request.user.id, is_main=True).name,
                    like_count          = 0,
                    view_count          = 0,
                    chat_count          = 0,
                    possible_discount   = request.data['possible_discount'],
                    introduction        = request.data['introduction'],
                    price               = request.data['price'],
                    )
            
            for image_dict in request.data['images']:
                for key, value in image_dict.items():
                    PostImage.objects.create(
                        post_id         = post.id,
                        url             = value,
                        )
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

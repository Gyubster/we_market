from rest_framework     import serializers

from user.models    import User
from post.models    import Post, PostImage

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model  = PostImage
        fields = ['url']

class PostSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True)
    
    class Meta:
        model        = Post
        fields       = ['title', 'subcategory', 'status', 'title', 'product', 'product', 'introduction', 'price', 'like_count', 'view_count', 'chat_count', 'possible_discount', 'address', 'created_at', 'updated_at', 'images']
        extra_kwargs = {
                'address'   : {'required': False},
                'images'    : {'required': False},
                }

class PostListSerializer(serializers.ModelSerializer):
    image = ImageSerializer(source='first_image', read_only=True)

    class Meta:
        model   = Post
        fields  = ['title', 'image','address', 'created_at', 'price', 'like_count', 'chat_count', 'product']

class PostDetailSerializer(serializers.ModelSerializer):
    images      = ImageSerializer(many=True, read_only=True)
    subcategory = serializers.ReadOnlyField(source='subcategory.name')
    writer      = serializers.SerializerMethodField()

    class Meta:
        model       = Post
        fields      = ['id', 'title', 'address', 'created_at', 'price', 'like_count', 'chat_count', 'images', 'subcategory', 'possible_discount', 'view_count', 'introduction', 'writer']

    def get_writer(self, obj):
        user = User.objects.get(id=obj.user_id)
        writer = {
                'writer_nickname'       : user.nickname,
                'wirter_profile_image'  : user.profile_image,
                'writer_posts'          : [
                    {
                        'title'         : post.title,
                        'post_image'    : post.images.first().url,
                        'price'         : post.price
                    } for post in Post.objects.filter(user_id=user.id)]
            }
        return writer   

from rest_framework     import serializers

from user.models    import User
from post.models    import Post, PostImage

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Post
        feilds = '__all__'

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model  = PostImage
        fields = ['url']

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
    

from rest_framework     import serializers

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

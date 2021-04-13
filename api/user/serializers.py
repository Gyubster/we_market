from django.contrib.auth            import get_user_model
from django.contrib.auth.models     import update_last_login

from rest_framework                  import serializers
from rest_framework_jwt.settings     import api_settings

from user.models    import User, Address, Filter
from post.models    import Subcategory

User                = get_user_model()
JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER  = api_settings.JWT_ENCODE_HANDLER

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model   = Address
        fields  = '__all__'

class FilterSerializer(serializers.ModelSerializer):
    class Meta:
        model   = Filter
        fields  = '__all__'

class UserSerializer(serializers.ModelSerializer):
    addresses = AddressSerializer(many=True, read_only=True)
    filters   = FilterSerializer(many=True, read_only=True)
    posts     = PostSerializer(manu=True, read_only=True)

    class Meta:
        model        = User
        excludes     = ('is_active', 'is_staff', 'is_superuser')
        extra_kwargs = {
                'phone_number': {'validators':[]}
                }

    def validate(self, data):
        print(data)
        user, is_created = User.objects.get_or_create(phone_number=data["phone_number"])
        
        if is_created:
            subcategory_ids = Subcategory.objects.filter(category_id=1).values_list('id', flat=True)
            Filter.objects.bulk_create([Filter(user_id=user.id, subcategory_id=subcategory_id)for subcategory_id in subcategory_ids])
        
        paylaod      = JWT_PAYLOAD_HANDLER(user)
        access_token = JWT_ENCODE_HANDLER(paylaod)

        update_last_login(None, User)

        results = {
                'phone_number': user.phone_number,
                'access_token': access_token,
                }
        
        return results

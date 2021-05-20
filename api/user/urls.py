from django.urls    import path

from .views import UserSignInGenericAPIView, AddressDetailGenericAPIView

app_name= 'users'

urlpatterns = [
    path('/signin', UserSignInGenericAPIView.as_view(), name='user-signin'),
    path('/address', AddressDetailGenericAPIView.as_view(), name='user-address'),
]

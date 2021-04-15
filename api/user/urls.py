from django.urls    import path

from .views import AddressDetailGenericsView, UserSignInGenericsView

app_name= 'users'

urlpatterns = [
    path('/signin', UserSignInGenericsView.as_view(), name='user-signin'),
    path('/address', AddressDetailGenericsView.as_view(), name='user-address'),
]

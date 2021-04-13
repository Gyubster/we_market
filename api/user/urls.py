from django.urls    import path

from .views import UserSignInGenericsView

app_name= 'users'

urlpatterns = [
    path('/signin', UserSignInGenericsView.as_view(), name='user-signin'),
]

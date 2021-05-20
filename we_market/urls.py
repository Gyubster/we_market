from django.contrib import admin
from django.urls    import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user', include('api.user.urls'), name='user-api'),
    path('api/post', include('api.post.urls'), name='post-api'),
]

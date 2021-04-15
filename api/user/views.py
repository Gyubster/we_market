from rest_framework                 import status, generics
from rest_framework.response        import Response
from rest_framework.permissions     import IsAdminUser,IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny

from user.models    import User, Filter, Address

from .serializers   import UserAddressSerialzier, UserSerializer

class AddressDetailGenericsView(generics.RetrieveAPIView):
    queryset            = User.objects.all()
    serializer_class    = UserAddressSerialzier
    permission_classes  = [AllowAny]

    def retrieve(self, request, *args, **kwargs):
        instance    = User.objects.get(id=request.user.id)
        serializer  = self.get_serializer(instance)
        return Response(serializer.data)

class UserSignInGenericsView(generics.GenericAPIView):
    queryset            = User.objects.all()
    serializer_class    = UserSerializer
    permission_classes  = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)

        if not serializer.is_valid(raise_exception=True):
            return Response({"message": "Request Body Error."}, status=status.HTTP_409_CONFLICT)

        response = {           
            'access_token'  : serializer.validated_data['access_token']
        }

        return Response(response, status=status.HTTP_200_OK)

from rest_framework                 import status, generics, mixins
from rest_framework.response        import Response
from rest_framework.permissions     import IsAdminUser,IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny

from user.models    import User, Filter, Address

from .serializers   import AddressSerializer, UserSerializer

class AddressDetailGenericAPIView(generics.ListAPIView):
    queryset            = Address.objects.all()
    serializer_class    = AddressSerializer
    permission_classes  = [AllowAny]

    def get_queryset(self):
        return Address.objects.filter(user_id=self.request.user.id)

    def post(self, request):
        serializer  = AddressSerializer(data=request.data)
        user        = User.objects.get(id=request.user.id)

        if not serializer.is_valid(raise_exception=True):
            return Response({"message": "Request Body Error."}, status=status.HTTP_409_CONFLICT)

        name = serializer.validated_data['name']
        if name == "None":
            return Response({'message': 'fail'}, status=status.HTTP_200_OK)
        
        try:
            former_address  = Address.objects.get(user_id=user.id, name=name, is_main=False)
            present_address = Address.objects.get(user_id=user.id, is_main=True)
            
            present_address.is_main = False
            former_address.is_main  = True
            
            present_address.save()
            former_address.save()
            
        except Address.DoesNotExist:
            try :
                former_address = Address.objects.get(user_id=user.id, is_main=True)
                former_address.is_main = False
                former_address.save()
                Address.objects.create(
                    user_id = user.id,
                    name    = name,
                    is_main = True
                )
            except Address.DoesNotExist:
                Address.objects.create(
                    user_id = user.id,
                    name    = name,
                    is_main = True
                )

        return Response({'message':'success'}, status=status.HTTP_200_OK)

class UserSignInGenericAPIView(generics.GenericAPIView):
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

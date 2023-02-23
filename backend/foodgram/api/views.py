from djoser.views import UserViewSet
from .serializers import CustomUserSerializer
from django.contrib.auth import get_user_model


User = get_user_model()


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer

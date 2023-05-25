from djoser.serializers import UserCreateSerializer


class MyUserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        fields = ["id", "email", "first_name", "last_name", "password", "username"]
        
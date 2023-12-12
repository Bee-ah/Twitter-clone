from rest_framework.views import APIView
from requests import Response
from rest_framework import serializers
from social.models.social import Profile, User
from rest_framework.views import status

#the aim was to practice serializer

#to get list of profiles
class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    def get_user(self, profile):
        user_data = {
            "id": profile.user.id,
            "username": profile.user.username,
        }
        return user_data

    class Meta:
        model = Profile
        fields = ["user", "profile_image", "date", "profile_bio"]

#to register user
class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)

    def validate(self, attrs):
        username = attrs.get("username")
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError({"username": "Username already exists"})
        return attrs

    def create(self, validated_data):
        user = User(
            username=validated_data["username"],
        )
        user.set_password(validated_data["password"])
        user.save()
        return user


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"user": user.id})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

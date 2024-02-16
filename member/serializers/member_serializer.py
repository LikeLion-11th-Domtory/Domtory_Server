from rest_framework import serializers
from member.domains import Member
from utils.validators import validate_password, validate_email, validate_nickname, ERROR_MESSAGE

class SignupRequestSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(validators=[validate_email], error_messages=ERROR_MESSAGE)
    password = serializers.CharField(validators=[validate_password], error_messages=ERROR_MESSAGE)
    nickname = serializers.CharField(validators=[validate_nickname], error_messages=ERROR_MESSAGE)
    phoneNumber = serializers.CharField(source='phone_number', error_messages=ERROR_MESSAGE)
    dormitoryCard = serializers.ImageField(source='dormitory_card', error_messages=ERROR_MESSAGE)
    dormitoryCode = serializers.CharField(source='dormitory_code', error_messages=ERROR_MESSAGE)
    name = serializers.CharField(error_messages=ERROR_MESSAGE)
    birthday = serializers.DateTimeField(error_messages=ERROR_MESSAGE)

    class Meta:
        model = Member
        fields = ('email', 'password', 'name', 'phoneNumber', 'nickname', 'birthday', 'dormitoryCode', 'dormitoryCard')
    
class SigninRequestSerialzier(serializers.ModelSerializer):
    username = serializers.CharField(validators=[])

    class Meta:
        model = Member
        fields = ('username', 'password')

class _MemberResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ('id', 'username')

class SigninResponseSerializer(serializers.Serializer):
    accessToken = serializers.CharField(source='access_token')
    refreshToken = serializers.CharField(source='refresh_token')
    member = _MemberResponseSerializer()

class PasswordChangeRequestSerializer(serializers.Serializer):
    oldPassword = serializers.CharField(source='old_password', error_messages=ERROR_MESSAGE)
    newPassword = serializers.CharField(validators=[validate_password], error_messages=ERROR_MESSAGE, source='new_password')
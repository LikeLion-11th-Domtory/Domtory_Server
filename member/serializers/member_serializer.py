from rest_framework import serializers

from dorm.domains import DormList
from member.domains import Member
from utils.validators import validate_password, validate_email, validate_nickname, validate_duplicated_signup, ERROR_MESSAGE

"""
deprecated
"""
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

class SignupRequestSerializerV2(serializers.ModelSerializer):
    phone_number = serializers.CharField(error_messages=ERROR_MESSAGE)
    dorm = serializers.ChoiceField(choices=DormList.get_names(), error_messages=ERROR_MESSAGE)
    dormitory_code = serializers.CharField(validators=[], error_messages=ERROR_MESSAGE)
    name = serializers.CharField(error_messages=ERROR_MESSAGE)
    birthday = serializers.CharField(error_messages=ERROR_MESSAGE)

    class Meta:
        model = Member
        fields = ('name', 'phone_number', 'dorm', 'birthday', 'dormitory_code')

    def validate(self, data):
        validate_duplicated_signup(data['dormitory_code'], data['dorm'])
        return data
    
class SigninRequestSerialzier(serializers.ModelSerializer):
    dormitory_code = serializers.CharField(validators=[], error_messages=ERROR_MESSAGE)
    dorm = serializers.ChoiceField(choices=DormList.get_names(), error_messages=ERROR_MESSAGE)
    password = serializers.CharField(error_messages=ERROR_MESSAGE)

    class Meta:
        model = Member
        fields = ('dormitory_code', 'dorm', 'password')

class MemberInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ('id', 'dormitory_code', 'phone_number', 'name', 'dorm', 'birthday', 'status', 'is_staff', 'is_superuser')

class _MemberResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ('id', 'dormitory_code', 'dorm', 'name', 'is_staff')

class SigninResponseSerializer(serializers.Serializer):
    accessToken = serializers.CharField(source='access_token')
    refreshToken = serializers.CharField(source='refresh_token')
    member = _MemberResponseSerializer()

class PasswordChangeRequestSerializer(serializers.Serializer):
    oldPassword = serializers.CharField(source='old_password', error_messages=ERROR_MESSAGE)
    newPassword = serializers.CharField(validators=[validate_password], error_messages=ERROR_MESSAGE, source='new_password')
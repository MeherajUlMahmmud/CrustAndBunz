from rest_framework import serializers
from web_app.models import *


class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['id', 'name', 'email', 'is_active', 'token']


class ProfileModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileModel
        fields = "__all__"


class FeedbackModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedbackModel
        fields = "__all__"

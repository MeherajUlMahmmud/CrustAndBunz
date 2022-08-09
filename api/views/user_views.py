from django.core.files.base import ContentFile
import base64

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND

from rest_framework.authtoken.models import Token

from web_app.models import *

from django.contrib.auth import authenticate
from django.utils.text import slugify

from api.serializers import user_serializer


@api_view(['POST'])
def login_view(request):
    data = request.data
    email = data['email']
    password = data['password']
    print(email, password)

    try:
        auth_user = authenticate(email=email, password=password)
    except:
        return Response({"error": "Invalid Credentials"}, status=HTTP_400_BAD_REQUEST)

    if auth_user and auth_user.is_active:
        return Response({"token": auth_user.token}, status=HTTP_200_OK)
    elif auth_user and not auth_user.is_active:
        return Response({"error": "Your account is suspended"}, status=HTTP_400_BAD_REQUEST)
    else:
        return Response({"error": "Invalid Credentials"}, status=HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def signup_view(request):
    data = request.data
    name = data['name']
    email = data['email']
    password = data['password']
    print(name, email, password)
    try:
        user = UserModel.objects.create_user(
            name=name, email=email, password=password)
        slug_str = "%s %s" % (user.name, user.id)
        slug = slugify(slug_str)
        user.slug = slug
        token, created = Token.objects.get_or_create(user=user)
        user.token = token.key
        user.save()
        ProfileModel.objects.create(user=user)
        CartModel.objects.create(user=user)

        return Response({"token": token.key}, status=HTTP_200_OK)
    except:
        return Response({"error": "User already exists"}, status=HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile_view(request):  # profile view
    user = UserModel.objects.get(id=request.user.id)
    profile = ProfileModel.objects.get(user=user)

    serialized_user = user_serializer.UserModelSerializer(user, many=False).data
    serialized_profile = user_serializer.ProfileModelSerializer(profile, many=False).data

    return Response({"user": serialized_user, "profile": serialized_profile}, status=HTTP_200_OK)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user(request):  # edit profile view
    data = request.data
    name = data['name']
    email = data['email']

    try:
        user = UserModel.objects.get(id=request.user.id)
        if user.name != name:
            user.name = name

        if user.email != email:
            user.email = email

        user.save()
        return Response(status=HTTP_200_OK)
    except:
        return Response(status=HTTP_404_NOT_FOUND)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    data = request.data
    phone = data['phone']
    address = data['address']

    user = UserModel.objects.get(id=request.user.id)
    profile = ProfileModel.objects.get(user=user)
    profile.phone = phone
    profile.address = address
    profile.save()
    return Response({"message": "Profile updated successfully"}, status=HTTP_200_OK)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_profile_image(request):
    data = request.data
    file = data["file"]
    name = data["name"]

    image_file = ContentFile(base64.b64decode(file), name)

    user = UserModel.objects.get(id=request.user.id)
    profile = ProfileModel.objects.get(user=user)
    profile.image = image_file
    profile.save()
    profile = ProfileModel.objects.get(user=user)

    serialized_user_data = user_serializer.UserModelSerializer(user, many=False).data
    serialized_profile_data = user_serializer.ProfileModelSerializer(profile, many=False).data
    return Response({"user": serialized_user_data, "profile": serialized_profile_data}, status=HTTP_200_OK)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_password(request):
    data = request.data
    old_password = data['old_password']
    new_password = data['new_password']
    try:
        user = UserModel.objects.get(id=request.user.id)
        auth = authenticate(email=user.email, password=old_password)
        if auth:
            user.set_password(new_password)
            user.save()
            return Response({"message": "Password updated successfully"}, status=HTTP_200_OK)
        else:
            return Response({"message": "Old password is incorrect"}, status=HTTP_400_BAD_REQUEST)
    except:
        return Response({"message": "Error occured"}, status=HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def reset_password(request):
    data = request.data
    new = data['new_password']
    pass


@api_view(['POST'])
def feedback_view(request):
    data = request.data
    if data['name'] and data['email'] and data['subject'] and data['message']:
        feedback = FeedbackModel(
            name=data['name'], email=data['email'], subject=data['subject'], message=data['message'])
        feedback.save()
        return Response(HTTP_200_OK)
    else:
        return Response(HTTP_400_BAD_REQUEST)

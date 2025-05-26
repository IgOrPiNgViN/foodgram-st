from djoser.views import UserViewSet
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User, Subscription
from .serializers import (
    CustomUserCreateSerializer,
    CustomUserSerializer,
    SetAvatarSerializer,
    SetPasswordSerializer,
    SubscriptionSerializer,
)

class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer

    def get_serializer_class(self):
        if self.action == "create":
            return CustomUserCreateSerializer
        return CustomUserSerializer

    def get_permissions(self):
        if self.action in [
            "retrieve",
        ]:
            return [AllowAny()]
        return super().get_permissions()

    @action(
        detail=False,
        methods=["get"],
        permission_classes=[permissions.IsAuthenticated],
    )
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(
        detail=False,
        methods=["post"],
        permission_classes=[permissions.IsAuthenticated],
    )
    def set_password(self, request):
        serializer = SetPasswordSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            user = request.user
            user.set_password(serializer.validated_data["new_password"])
            user.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=False,
        methods=["put", "delete"],
        permission_classes=[permissions.IsAuthenticated],
    )
    def avatar(self, request):
        if request.method == "DELETE":
            user = request.user
            user.avatar = None
            user.save()
            return Response(status=status.HTTP_204_NO_CONTENT)

        if "avatar" not in request.data or not request.data["avatar"]:
            return Response(
                {"avatar": ["This field is required."]},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = SetAvatarSerializer(
            request.user,
            data=request.data,
            partial=True,
            context={"request": request},
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=False,
        methods=["get"],
        permission_classes=[permissions.IsAuthenticated],
    )
    def subscriptions(self, request):
        user = request.user
        subscriptions = Subscription.objects.filter(user=user)
        page = self.paginate_queryset(subscriptions)
        serializer = SubscriptionSerializer(page, many=True, context={"request": request})
        return self.get_paginated_response(serializer.data)

    @action(
        detail=True,
        methods=["post"],
        permission_classes=[permissions.IsAuthenticated],
    )
    def subscribe(self, request, id=None):
        user = request.user
        author = self.get_object()
        if Subscription.objects.filter(user=user, author=author).exists():
            return Response({"errors": "Вы уже подписаны на этого пользователя."}, status=status.HTTP_400_BAD_REQUEST)
        if user == author:
            return Response({"errors": "Нельзя подписаться на самого себя."}, status=status.HTTP_400_BAD_REQUEST)
        subscription = Subscription.objects.create(user=user, author=author)
        serializer = SubscriptionSerializer(subscription, context={"request": request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(
        detail=True,
        methods=["delete"],
        permission_classes=[permissions.IsAuthenticated],
    )
    def unsubscribe(self, request, id=None):
        user = request.user
        author = self.get_object()
        subscription = Subscription.objects.filter(user=user, author=author)
        if subscription.exists():
            subscription.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"errors": "Вы не были подписаны на этого пользователя."}, status=status.HTTP_400_BAD_REQUEST)


class UserAvatarView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        if "avatar" not in request.data or not request.data["avatar"]:
            return Response(
                {"avatar": ["This field is required."]},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = SetAvatarSerializer(
            request.user,
            data=request.data,
            partial=True,
            context={"request": request},
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        user = request.user
        user.avatar = None
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.core.files.storage import default_storage
from ..models import UserFollow
from ..serializers.users import (
    UserWithDishesSerializer,
    FoodgramUserSerializer,
    UserProfilePicSerializer
)
from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework.pagination import LimitOffsetPagination  
from rest_framework.exceptions import NotAuthenticated
from .recipes import DishPagination

User = get_user_model()


class UserActionsViewSet(DjoserUserViewSet):
    pagination_class = LimitOffsetPagination  

    @action(detail=False, permission_classes=[IsAuthenticated])
    def me(self, request, *args, **kwargs):
        return super().me(request, *args, **kwargs)

    @action(detail=False, methods=['put', 'delete'], url_path='me/profile_pic', permission_classes=[IsAuthenticated])
    def profile_pic(self, request):
        user = request.user
        if request.method == "DELETE":
            if user.profile_pic:
                if hasattr(user.profile_pic, 'path') and user.profile_pic.name != "users/image.png":
                    default_storage.delete(user.profile_pic.path)
                elif user.profile_pic.name != "users/image.png":
                    user.profile_pic.delete(save=False)
                user.profile_pic = None
                user.save()
            return Response(status=status.HTTP_204_NO_CONTENT)

        serializer = UserProfilePicSerializer(user, data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        updated_user = serializer.save()
        profile_pic_url = request.build_absolute_uri(updated_user.profile_pic.url) if updated_user.profile_pic else None
        return Response({'profile_pic': profile_pic_url})


    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def following(self, request):
        user = request.user
        following_ids = UserFollow.objects.filter(follower=user).values_list('following_id', flat=True)
        following_users = User.objects.filter(id__in=following_ids)

        paginator = DishPagination()
        result_page = paginator.paginate_queryset(following_users, request)
        serializer = UserWithDishesSerializer(
            result_page, many=True, context={"request": request}
        )
        return paginator.get_paginated_response(serializer.data)
            
    
    @action(detail=True, methods=['post', 'delete'], permission_classes=[IsAuthenticated])
    def follow(self, request, id=None):
        user_to_follow = get_object_or_404(User, id=id)
        current_user = request.user

        if user_to_follow == current_user:
            return Response(
                {"errors": "Нельзя подписаться или отписаться от самого себя."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if request.method == "POST":
            follow, created = UserFollow.objects.get_or_create(
                follower=current_user,
                following=user_to_follow
            )
            if not created:
                return Response(
                    {"errors": f"Вы уже подписаны на пользователя {user_to_follow.login}."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            
            serializer = UserWithDishesSerializer(user_to_follow, context={"request": request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        try:
            follow_entry = UserFollow.objects.get(
                follower=current_user,
                following=user_to_follow
            )
        except UserFollow.DoesNotExist:
            return Response(
                {"errors": f"Вы не были подписаны на пользователя {user_to_follow.login}."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        follow_entry.delete()
        
        return Response(status=status.HTTP_204_NO_CONTENT)

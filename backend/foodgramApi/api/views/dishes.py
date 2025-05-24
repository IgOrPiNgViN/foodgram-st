from io import BytesIO
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated, SAFE_METHODS, BasePermission
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.contrib.auth import get_user_model
from django.db.models import Sum, Exists, OuterRef
from ..models import FavoriteDish, ShoppingList
from dishes.models import Dish, DishComponent
from ..serializers.dishes import (
    DishListSerializer,
    DishCreateSerializer,
    ShortDishSerializer
)
from django.template.loader import render_to_string
from weasyprint import HTML
from django.http import Http404, FileResponse
from django.urls import reverse

from django_filters.rest_framework import DjangoFilterBackend
import django_filters

User = get_user_model()

class DishFilter(django_filters.FilterSet):
    is_favorited = django_filters.CharFilter(method='filter_is_favorited')
    is_in_shopping_list = django_filters.CharFilter(method='filter_is_in_shopping_list')

    class Meta:
        model = Dish
        fields = ['creator', 'is_favorited', 'is_in_shopping_list']

    def filter_is_favorited(self, queryset, name, value):
        return self._filter_by_user_relation(
            queryset,
            relation='favorited_by_users_relations__user',
            value=value
        )

    def filter_is_in_shopping_list(self, queryset, name, value):
        return self._filter_by_user_relation(
            queryset,
            relation='in_shopping_lists_of_users__user',
            value=value
        )

    def _filter_by_user_relation(self, queryset, relation, value):
        user = self.request.user
        if not value or user.is_anonymous:
            return queryset

        true_values = {'1', 'true'}
        is_true = str(value).lower() in true_values

        if is_true:
            return queryset.filter(**{relation: user})
        return queryset.exclude(**{relation: user})


class DishPagination(PageNumberPagination):
    page_size = 6
    page_size_query_param = "limit"
    max_page_size = 100

class IsCreatorOrReadOnly(BasePermission):    
    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or obj.creator == request.user

class DishViewSet(viewsets.ModelViewSet):
    queryset = Dish.objects.all()
    pagination_class = DishPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = DishFilter

    def get_serializer_class(self):
        if self.action in ['create', 'partial_update', 'update']:
            return DishCreateSerializer
        if self.action in ['favorite', 'shopping_list'] and self.request.method == 'POST':
            return ShortDishSerializer 
        return DishListSerializer

    def get_permissions(self):
        if self.action in ['create', 'favorite', 'shopping_list', 'download_shopping_list']:
            self.permission_classes = [IsAuthenticated]
        elif self.action in ['partial_update', 'update', 'destroy']:
            self.permission_classes = [IsAuthenticated, IsCreatorOrReadOnly]
        elif self.action == 'get_link':
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [AllowAny]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)
        

    @action(detail=True, methods=['post', 'delete'], permission_classes=[IsAuthenticated])
    def favorite(self, request, pk=None):
        return self._handle_dish_action(
            request, pk, FavoriteDish, "избранном", "favorite"
        )

    @action(detail=True, methods=['post', 'delete'], permission_classes=[IsAuthenticated])
    def shopping_list(self, request, pk=None):
        return self._handle_dish_action(
            request, pk, ShoppingList, "списке покупок", "shopping_list"
        )

    def _handle_dish_action(self, request, pk, model, error_message, action_name):
        dish = get_object_or_404(Dish, pk=pk)
        user = request.user

        if request.method == 'POST':
            if model.objects.filter(user=user, dish=dish).exists():
                return Response(
                    {"error": f"Блюдо «{dish.title}» уже в {error_message}"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            model.objects.create(user=user, dish=dish)
            serializer = ShortDishSerializer(dish, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        entry = model.objects.filter(user=user, dish=dish)
        if not entry.exists():
            return Response(
                {"errors": f"Блюдо «{dish.title}» не было в {error_message}."},
                status=status.HTTP_400_BAD_REQUEST
            )
        entry.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def download_shopping_list(self, request):
        dish_ids = ShoppingList.objects.filter(user=request.user).values_list('dish_id', flat=True)
        
        components = (
            DishComponent.objects.filter(dish_id__in=dish_ids)
            .values("component__title", "component__unit")
            .annotate(total_quantity=Sum("quantity"))
            .order_by("component__title")
        )

        html = render_to_string("shopping_list.html", {"components": components})

        pdf_file = BytesIO(HTML(string=html, encoding="utf-8").write_pdf())

        response = FileResponse(pdf_file, as_attachment=True, filename="shopping_list.pdf", content_type="application/pdf")
        return response

    @action(detail=True, methods=['get'], permission_classes=[AllowAny], url_path='get-link', url_name='get-link')
    def get_link(self, request, pk=None):
        dish = self.get_object()

        short_link = request.build_absolute_uri(f'/api/s/{pk}')

        return Response(
            {"short-link": short_link},
            status=status.HTTP_200_OK
        )
        
    @action(detail=False, methods=['get'], permission_classes=[AllowAny], url_path='s', url_name='short')
    def short_link(self, request, hash=None):
        dish = get_object_or_404(Dish, pk=hash)
        serializer = self.get_serializer(dish)
        return Response(serializer.data)


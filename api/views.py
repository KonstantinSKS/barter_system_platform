from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view, inline_serializer

from rest_framework import viewsets, generics, status, serializers, permissions
from rest_framework.authtoken.models import Token
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from ads import models
from api import serializers as srlzs
from api.filters import AdFilter, ExchangeProposalFilter


@extend_schema(
    tags=[('Пользователи')],
    summary=('Регистрация пользователя'),
)
class RegistrationView(generics.CreateAPIView):
    """Регистрация пользователя в системе.
    Требуется отправить логин, почту и пароль."""

    permission_classes = (AllowAny,)
    serializer_class = srlzs.UserSignUpSerializer


@extend_schema(
    tags=['Пользователи'],
    request=srlzs.UserLoginSerializer,
    responses={200: {'type': 'object',
                     'properties': {'token': {'type': 'string'}}}},
    summary='Вход в систему'
)
class LoginView(APIView):
    """Вход в систему по логину и паролю.
    Возвращает статус 200 и токен для авторизации."""

    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = srlzs.UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})


@extend_schema(
    tags=['Пользователи'],
    summary='Выход из системы'
)
class LogoutView(APIView):
    """Выход из системы.
    Возвращает статус 200 и сообщение 'Выход выполнен'."""

    permission_classes = (IsAuthenticated,)

    def post(self, request):
        request.user.auth_token.delete()
        return Response(
            {'message': 'Выход выполнен'}, status=status.HTTP_200_OK
        )


@extend_schema(
    tags=['Пользователи'],
    summary='Данные о пользователе',
    responses={
        200: inline_serializer(
            name='successful_responses',
            fields={
                "id": serializers.IntegerField(),
                "username": serializers.CharField(),
                "email": serializers.EmailField()
            },
        ),
    },
)
class MeView(APIView):
    """Возвращает пользователю его данные."""

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        return Response({
            'id': user.id,
            'username': user.username,
            'email': user.email,
        })


@extend_schema(tags=['Объявления'])
@extend_schema_view(
    retrieve=extend_schema(
        summary='Просмотр информации объявления по id записи.',
        description='Возвращает объект объявления по id.',
    ),
    list=extend_schema(
        summary='Просмотр списка объявлений.',
        description='Возвращает список объектов объявлений.',
    ),
    create=extend_schema(
        summary='Создание объявления (Доступно только авторизованному пользователю).',
        description='Создание объекта объявления (все поля, кроме image_url, обязательны)',
    ),
    partial_update=extend_schema(
        summary='Частичное обновление объявления (Доступно только авторизованному автору).',
        description='Частичное обновление объекта объявления по id (возможно изменение одного или сразу нескольких полей)',
    ),
    destroy=extend_schema(
        summary='Удаление объвления (Доступно только авторизованному автору).',
        description='Удаляет объект объявления по id.',
    ),
)
class AdViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с объектами модели Ad.
    Методы POST, GET, PATCH, DELETE."""

    http_method_names = ['get', 'post', 'patch', 'delete']
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['title', 'description']
    filterset_class = AdFilter
    queryset = models.Ad.objects.all()

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return srlzs.AdReadSerializer
        return srlzs.AdCreateSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@extend_schema(tags=['Категории объявлений'])
@extend_schema_view(
    retrieve=extend_schema(
        summary='Просмотр информации о категории по id записи.',
    ),
    list=extend_schema(
        summary='Просмотр списка категорий.',
    ),
)
class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для чтения/получения категорий."""

    queryset = models.Category.objects.all()
    serializer_class = srlzs.CategorySerializer
    permission_classes = (permissions.AllowAny,)


@extend_schema(tags=['Предложения обмена'])
@extend_schema_view(
    retrieve=extend_schema(
        summary='Просмотр информации предложения по id записи.',
        description='Возвращает объект предложения по id (только когда текущий пользователь — как отправитель, так и получатель).',
    ),
    list=extend_schema(
        summary='Просмотр списка предложений.',
        description='Возвращает все предложения, в которых текущий пользователь — как отправитель, так и получатель.',
    ),
    create=extend_schema(
        summary='Создание предложения (Доступно только авторизованному пользователю).',
        description=('Создание объекта предложения по id ябъявления отправителя и id объявление получателя<br>'
                     '(все поля, кроме comment, обязательны)'),
    ),
    partial_update=extend_schema(
        summary='Частичное обновление предложения (Доступно только авторизованному автору).',
        description=('Частичное обновление объекта предложения по id: изменение статуса предложения (например, «принята» или «отклонена»<br>'
                     'При этом изменить статус может только получатель предложения'),
    ),
    destroy=extend_schema(
        summary='Удаление предложения (Доступно только авторизованному автору).',
        description='Удаляет объект предложения по id.',
    ),
)
class ExchangeProposalViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с объектами модели ExchangeProposal.
    Методы POST, GET, PATCH, DELETE."""

    http_method_names = ['get', 'post', 'patch', 'delete']
    filter_backends = [DjangoFilterBackend]
    filterset_class = ExchangeProposalFilter
    queryset = models.ExchangeProposal.objects.none()

    def get_queryset(self):
        user = self.request.user
        return models.ExchangeProposal.objects.filter(
            Q(ad_sender__user=user) | Q(ad_receiver__user=user)
        )

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return srlzs.ProposalReadSerializer
        if self.action == 'partial_update':
            return srlzs.ProposalUpdateSerializer
        return srlzs.ProposalCreateSerializer

    def partial_update(self, request, *args, **kwargs):
        """Менять статус может только получатель предложения."""

        instance = self.get_object()

        if instance.ad_receiver.user != request.user:
            return Response(
                {"detail": "Вы можете менять статус только входящего предложения!"},
                status=status.HTTP_403_FORBIDDEN
            )

        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """Удалять предложения может только автор."""

        instance = self.get_object()

        if instance.ad_sender.user != request.user:
            return Response(
                {"detail": "Удаление доступно только автору предложения."},
                status=status.HTTP_403_FORBIDDEN
            )

        return super().destroy(request, *args, **kwargs)

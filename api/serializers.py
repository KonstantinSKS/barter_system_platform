from django.core.validators import FileExtensionValidator
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from rest_framework import serializers

from ads import models
from ads import choices as chcs
from config import constants
from users.models import User


class UserSignUpSerializer(serializers.ModelSerializer):
    """Сериализатор регистрации пользователя."""

    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(
        write_only=True,
        validators=[validate_password]
    )

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'password',
        )

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserLoginSerializer(serializers.Serializer):
    """Сериализатор входа пользователя в систему."""

    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(
            username=data['username'],
            password=data['password']
        )
        if not user:
            raise serializers.ValidationError("Неверные учетные данные")
        data['user'] = user
        return data


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для модели Category."""

    class Meta:
        model = models.Category
        fields = (
            'id',
            'title',
            'description',
        )


class AdCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания, обновления модели Ad."""

    user = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )
    image_url = serializers.ImageField(
        required=False,
        allow_null=True,
        validators=[
            FileExtensionValidator(
                allowed_extensions=constants.IMAGE_EXTENSIONS)],
    )
    category = serializers.PrimaryKeyRelatedField(
        queryset=models.Category.objects.all()
    )
    condition = serializers.ChoiceField(
        choices=chcs.AD_CONDITION_CHOICES
    )

    class Meta:
        model = models.Ad
        fields = (
            'id',
            'title',
            'description',
            'user',
            'image_url',
            'category',
            'condition',
            'created_at',
        )


class AdReadSerializer(serializers.ModelSerializer):
    """Сериализатор для чтения модели Ad."""

    user = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )
    category = CategorySerializer()

    class Meta:
        model = models.Ad
        fields = (
            'id',
            'title',
            'description',
            'user',
            'image_url',
            'category',
            'condition',
            'created_at',
        )


class ProposalReadSerializer(serializers.ModelSerializer):
    """Сериализатор для чтения модели ExchangeProposal."""

    ad_sender = AdReadSerializer()
    ad_receiver = AdReadSerializer()

    class Meta:
        model = models.ExchangeProposal
        fields = (
            'id',
            'ad_sender',
            'ad_receiver',
            'comment',
            'status',
            'created_at',
        )


class ProposalCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания модели ExchangeProposal."""

    ad_sender = serializers.PrimaryKeyRelatedField(
        queryset=models.Ad.objects.all()
    )
    ad_receiver = serializers.PrimaryKeyRelatedField(
        queryset=models.Ad.objects.all()
    )
    comment = serializers.CharField(
        required=False, allow_blank=True, allow_null=True
    )
    status = serializers.ChoiceField(
        choices=chcs.PROPOSAL_STATUS_CHOICES,
        read_only=True
    )

    class Meta:
        model = models.ExchangeProposal
        fields = (
            'id',
            'ad_sender',
            'ad_receiver',
            'comment',
            'status',
            'created_at',
        )
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=models.ExchangeProposal.objects.all(),
                fields=('ad_sender', 'ad_receiver'),
                message='Вы уже создали предложение обмена на это объявление!'
            )
        ]

    def validate(self, data):
        request_user = self.context['request'].user
        ad_sender = data.get('ad_sender')
        ad_receiver = data.get('ad_receiver')

        if ad_sender.user != request_user:
            raise serializers.ValidationError("Вы можете предложить обмен только от своего объявления!")

        if ad_receiver.user == request_user:
            raise serializers.ValidationError("Нельзя отправить предложение на своё же объявление!")

        return data


class ProposalUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор для изменения статуса предложения ExchangeProposal."""

    status = serializers.ChoiceField(choices=chcs.PROPOSAL_STATUS_CHOICES)

    class Meta:
        model = models.ExchangeProposal
        fields = ('status',)

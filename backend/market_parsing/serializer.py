from .models import *
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from django.contrib.auth.models import User

class PriceLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceLink
        fields = ('price', 'data_parser_price')

class LinkSerializer(serializers.ModelSerializer):
    price_link = PriceLinkSerializer(many=True, read_only=True)
    class Meta:
        model = Link
        fields = ('id','link', 'price_link', 'comment')

class UserSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super(UserSerializer, self).__init__(*args, **kwargs)

        if 'labels' in self.fields:
            raise RuntimeError(
                'You cant have labels field defined '
                'while using MyModelSerializer'
            )

        self.fields['labels'] = SerializerMethodField()

    def get_labels(self, *args):
        labels = {}

        for field in self.Meta.model._meta.get_fields():
            if field.name in self.fields:
                labels[field.name] = field.verbose_name

        return labels
    class Meta:
        model = User
        fields = ('username','first_name',
                  'last_name', 'email')


class UpdateUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
        }

    def update(self, instance, validated_data):
        if 'email' in validated_data:
            try:
                user = User.objects.get(email=validated_data['email'])
                if instance.username != user.username:
                    raise serializers.ValidationError(
                        {'email': 'Этот email уже используется'})
            except User.DoesNotExist:
                pass
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance

class ChangePasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "password"]
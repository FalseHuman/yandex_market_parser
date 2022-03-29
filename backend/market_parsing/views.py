from email.headerregistry import Group
from django.shortcuts import render
from rest_framework import generics, viewsets, parsers, views, permissions
from . import models, serializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from .models import *
from .serializer import *
from django.contrib.auth.models import User
from rest_framework import status
from uuid import uuid4
from django.core.mail import send_mail
from core.settings import EMAIL_HOST_USER
from django.utils.datastructures import MultiValueDictKeyError


class TokenGet(APIView):
    def post(self, request, format=None):
        try:
            Token.objects.get(key=request.data['auth-token'])
            return Response({"token": "exists"}, status=status.HTTP_200_OK)
        except Token.DoesNotExist:
            return Response({"token": "not exists"}, status=status.HTTP_400_BAD_REQUEST)


class CheckEmail(APIView):
    def post(self, request, format=None):
        # print(User.objects.get(email=request.data['email']))
        try:
            user = User.objects.get(email=request.data['email'])
            rand_token = uuid4()
            TokenReset.objects.create(token_for_user=user, token=rand_token)
            subject, message = "Восстановление пароля", f"Здравствуйте, {user.username} \nТокен для восстановления пароля - {rand_token} Вставьте токен в форму без пробелов\nЕсли это были не вы просто проигнорируйте данное сообщение"
            send_mail(
                subject,
                message,
                EMAIL_HOST_USER,
                [f"{user.email}"],
                fail_silently=False,
            )
            return Response(status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"email": "Пользователя с таким адресом эл.почты не существует или некорректно введён адрес."}, status=status.HTTP_400_BAD_REQUEST)


class CheckToken(APIView):
    def post(self, request, format=None):
        try:
            token = TokenReset.objects.get(token=request.data['token'])
            token.delete()
            return Response(status=status.HTTP_200_OK)
        except TokenReset.DoesNotExist:
            return Response({"token": "Токен введён не правильно."}, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, ]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        #print('user', self.request.user)
        return User.objects.filter(username=self.request.user)


class UpdateProfileView(generics.UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = UpdateUserSerializer

    def put(self, request, format=None):
        serializer = UpdateUserSerializer(
            data=request.data, instance=request.user)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GroupView(viewsets.ModelViewSet):
    """ CRUD Group
    """
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = serializer.GroupSerializer
    def get_queryset(self):
        return GroupLink.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)




class LinkView(viewsets.ModelViewSet):
    """ CRUD Links
    """
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = serializer.LinkSerializer



    def get_queryset(self):
        params = self.request.query_params.copy()
        data = {
                'user': self.request.user,
            }
        for i in params:
            print(params[i]!='null')
            try:
                if params[i]!= 'null' and params[i]!='':
                    data[i] = params[i]
            except MultiValueDictKeyError:
                pass
        print(data)
        return Link.objects.filter(**data)

    def perform_create(self, serializer):
        #print(self.request)
        serializer.save(user=self.request.user)

class AnalogLinkView(viewsets.ModelViewSet):
    """ CRUD AnalogLinks
    """
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = serializer.AnalogLinkSerializer

    def get_queryset(self):
        return AnalogLink.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ChangePasswordView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = ChangePasswordSerializer

    @action(detail=True, methods=['post'])
    def change_password(self, request, pk=None):
        """ Код с курса https://stepik.org/lesson/334150/step/5?unit=317559 """
        def is_password_good(password):
            count, count1, count2 = 0, 0, 0
            for i in range(len(password)):
                if '0' <= password[i] <= '9':
                    count += 1
                if 'A' <= password[i] <= 'Z':
                    count1 += 1
                if 'a' <= password[i] <= 'z':
                    count2 += 1
            return len(password) >= 8 and count >= 1 and count1 >= 1 and count2 >= 1
        user = User.objects
        try:
            username = user.get(username=request.data.get("login"))
            print(request.data.get("password_1") ==
                  request.data.get("password_2"))
            if request.data.get("password_1") == request.data.get("password_2"):
                if is_password_good(request.data.get("password_1")) == True:
                    username.set_password(request.data.get("password_1"))
                    username.save()
                else:
                    message = "Введённый пароль слишком короткий. Он должен содержать как минимум 8 символов. Он должен содержать  заглавную букву. Введённый пароль слишком широко распространён. Введённый пароль состоит только из цифр."
                    return Response({'password_1': message, 'password_2': message}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'password_1': "Пароли не совпадают.", 'password_2': "Пароли не совпадают."}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'login': "Пользователь не существует."}, status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_200_OK)

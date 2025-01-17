from django.db import IntegrityError
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import login
from .models import Profile, Report
from .permissions import ProfilePermissions, UserPermissions, ReportPermissions
from .serializers import ProfileSerializer, UserSerializer, ReportSerializer


class UserAPIViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (UserPermissions,)

    def create(self, request, *args, **kwargs):
        user = User.objects.create(
            username=request.data['username']
        )
        user.set_password(request.data['password'])
        user.save()
        login(request, user)
        return Response(
            {"username": user.username,
             "password": user.password},
            status=status.HTTP_201_CREATED)


class ProfileAPIViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (ProfilePermissions,)

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, args, kwargs)
        except IntegrityError as e:
            if 'UNIQUE constraint failed: api_profile.user_id' in e.args:
                return Response({'error': 'current user already has the profile'})
            else:
                return Response({'error': e.args})


class ReportAPIViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = (ReportPermissions,)

from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Profile, Project
from .serializers import ProfileSerializer, ProjectSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        else:
            self.permission_classes = [IsAuthenticated]

        return super().get_permissions()

    def retrieve(self, request, *args, **kwargs):
        if self.request.method == "GET":
            id = self.kwargs["pk"]
            profile = Profile.objects.get(id=id)
            return render(request, "profile_detail.html", {"profile": profile})

        return super().retrieve(request, *args, **kwargs)


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
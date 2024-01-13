from rest_framework.generics import (ListCreateAPIView,
                                     UpdateAPIView,
                                     RetrieveUpdateAPIView,
                                     RetrieveUpdateDestroyAPIView,
                                     ListAPIView)
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters import rest_framework as filters
from rest_framework.authtoken.views import ObtainAuthToken

from projects.models import Project
from .serializers import ProjectSerializer, ProjectListSerializer


class ProjectAPIList(ListCreateAPIView):
    queryset = Project.objects.prefetch_related('tasks')
    serializer_class = ProjectListSerializer
    filterset_fields = ('is_active',)
    permission_classes = (IsAuthenticatedOrReadOnly,)


# class ProjectAPIUpdate(UpdateAPIView):
#     queryset = Project.objects.all()
#     serializer_class = ProjectListSerializer
#     permission_classes = (IsAuthenticatedOrReadOnly,)


class ProjectAPIDetailView(RetrieveUpdateAPIView):
    queryset = Project.objects.prefetch_related('tasks')
    serializer_class = ProjectSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


# class ProjectViewSet(ModelViewSet):
#     queryset = Project.objects.prefetch_related('tasks')
#     serializer_class = ProjectSerializer
#     filter_backends = (filters.DjangoFilterBackend,)
#     filterset_fields = ('is_active',)

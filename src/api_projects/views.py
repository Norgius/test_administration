from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from rest_framework.filters import SearchFilter
from drf_spectacular.utils import extend_schema_view, extend_schema

from projects.models import Project, Task, Employee, Comment
from . import serializers
from .filters import TaskFilter, ProjectFilter


@extend_schema_view(
    list=extend_schema(summary="Получить список проектов", tags=['Проекты']),
    create=extend_schema(summary="Создание нового проекта", tags=['Проекты']),
)
class ProjectListAPI(mixins.ListModelMixin,
                     mixins.CreateModelMixin,
                     GenericViewSet):
    queryset = Project.objects.prefetch_related('tasks')
    serializer_class = serializers.ProjectListSerializer
    filterset_class = ProjectFilter


@extend_schema_view(
    retrieve=extend_schema(summary="Найти проект по его id", tags=['Проекты']),
    partial_update=extend_schema(summary="Изменить проект частично", tags=['Проекты']),
)
class ProjectDetailsAPI(mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin,
                        GenericViewSet):
    queryset = Project.objects.prefetch_related('tasks')
    serializer_class = serializers.ProjectDetailsSerializer
    http_method_names = ['get', 'patch']


@extend_schema_view(
    list=extend_schema(summary="Получить список задач", tags=['Задачи']),
    create=extend_schema(summary="Создание новой задачи", tags=['Задачи']),
)
class TaskListAPI(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  GenericViewSet):
    queryset = Task.objects.get_all_joins()
    serializer_class = serializers.TaskListSerializer
    filterset_class = TaskFilter


@extend_schema_view(
    retrieve=extend_schema(summary="Найти задачу по её id", tags=['Задачи']),
    partial_update=extend_schema(summary="Изменить задачу частично", tags=['Задачи']),
    destroy=extend_schema(summary="Удалить задачу", tags=['Задачи']),
)
class TaskDetailsAPI(mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     GenericViewSet):
    queryset = Task.objects.get_all_joins()
    serializer_class = serializers.TaskDetailsSerializer
    http_method_names = ['get', 'patch', 'delete']


@extend_schema_view(
    list=extend_schema(summary="Получить список сотрудников", tags=['Сотрудники']),
    create=extend_schema(summary="Добавление сотрудника в БД", tags=['Сотрудники']),
)
class EmployeeListAPI(mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      GenericViewSet):
    queryset = Employee.objects.all()
    serializer_class = serializers.EmployeeListSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name']


@extend_schema_view(
    retrieve=extend_schema(summary="Найти сотрудника по его id", tags=['Сотрудники']),
)
class EmployeeDetailsAPI(mixins.RetrieveModelMixin, GenericViewSet):
    queryset = Employee.objects.prefetch_related('tasks')
    serializer_class = serializers.EmployeeDetailsSerializer
    http_method_names = ['get']


@extend_schema_view(
    partial_update=extend_schema(
        summary="Частичное обновление данных о сотруднике",
        tags=['Сотрудники'],
        description='''Для привязки задач сотруднику необходимо передать список их `id`,
        если вы укажете те же задачи, которые уже привязаны к сотруднику,
        то связи между сотрудником и переданными задачами не станет.
        ''',
    ),
)
class EmployeeUpdateAPI(mixins.UpdateModelMixin, GenericViewSet):
    queryset = Employee.objects.prefetch_related('tasks')
    serializer_class = serializers.EmployeeUpdateSerializer
    http_method_names = ['patch']


@extend_schema_view(
    create=extend_schema(summary="Создать комментарий", tags=['Комментарии']),
    destroy=extend_schema(summary="Удалить комментарий", tags=['Комментарии']),
)
class CommentAPI(mixins.CreateModelMixin,
                 mixins.DestroyModelMixin,
                 GenericViewSet):
    queryset = Comment.objects.select_related('task')
    serializer_class = serializers.CommentSerializer

from rest_framework import serializers

from projects.models import Project, Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['name', 'description', 'deadline', 'status']


class ProjectSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ['name', 'description', 'is_active', 'tasks']


class ProjectListSerializer(serializers.ModelSerializer):
    tasks = serializers.SlugRelatedField(many=True, read_only=True, slug_field='name')

    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'is_active', 'tasks']

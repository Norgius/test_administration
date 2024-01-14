from rest_framework import serializers
from rest_framework.utils import model_meta

from projects.models import Project, Task, Employee, Comment


class TaskListSerializer(serializers.ModelSerializer):
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all(), write_only=True)

    class Meta:
        model = Task
        fields = ['id', 'name', 'description', 'deadline', 'status', 'project']


class ProjectDetailsSerializer(serializers.ModelSerializer):
    tasks = TaskListSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ['name', 'description', 'is_active', 'tasks']


class ProjectListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'is_active']


class CommentSerializer(serializers.ModelSerializer):
    task = serializers.PrimaryKeyRelatedField(queryset=Task.objects.all(), write_only=True)
    written_in = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'text', 'written_in', 'task']


class TaskDetailsSerializer(serializers.ModelSerializer):
    project = ProjectListSerializer(read_only=True)
    employees = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)
    comments = CommentSerializer(read_only=True, many=True)

    class Meta:
        model = Task
        fields = ['name', 'deadline', 'description', 'status', 'project', 'employees', 'comments']


class EmployeeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'name', 'position']


class EmployeeDetailsSerializer(serializers.ModelSerializer):
    tasks = TaskListSerializer(read_only=True, many=True)

    class Meta:
        model = Employee
        fields = ['name', 'position', 'tasks']


class EmployeeUpdateSerializer(serializers.ModelSerializer):
    tasks = serializers.PrimaryKeyRelatedField(queryset=Task.objects.all(), write_only=True, many=True)

    class Meta:
        model = Employee
        fields = ['name', 'position', 'tasks']

    def update(self, instance, validated_data):
        info = model_meta.get_field_info(instance)

        m2m_fields = []
        for attr, value in validated_data.items():
            if attr in info.relations and info.relations[attr].to_many:
                new_tasks, for_removing = [], []
                employee_tasks = instance.tasks.all()
                for item in value:
                    if item in employee_tasks:
                        for_removing.append(item)
                    else:
                        new_tasks.append(item)
                if for_removing:
                    [instance.tasks.remove(task) for task in for_removing]
                m2m_fields.append((attr, new_tasks))
            else:
                setattr(instance, attr, value)

        instance.save()

        for attr, value in m2m_fields:
            field = getattr(instance, attr)
            field.add(*value)

        return instance

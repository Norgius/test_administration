from django_filters import FilterSet, DateFilter, BooleanFilter

from projects.models import Task, Project


class TaskFilter(FilterSet):
    before_date = DateFilter(
        field_name="deadline",
        lookup_expr='lte',
        label='Задачи с deadlines до указанной даты (например: 2024-6-25)'
    )
    after_date = DateFilter(
        field_name="deadline",
        lookup_expr='gte',
        label='Задачи с deadlines после указанной даты (например: 2024-6-25)'
    )

    class Meta:
        model = Task
        fields = ['status', 'project']


class ProjectFilter(FilterSet):
    no_tasks = BooleanFilter(
        field_name="tasks",
        lookup_expr='isnull',
        label='При True показывает проекты, которые не имеют задач'
    )

    class Meta:
        model = Project
        fields = ['is_active']

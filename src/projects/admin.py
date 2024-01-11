from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from django.http.request import HttpRequest

from .models import Project, Task, Employee, Comment


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name']


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['name', 'deadline', 'status']
    list_display_links = ['name', 'deadline']
    list_filter = ['status']
    search_fields = ['name', 'project__name']
    readonly_fields = ['deadline']

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        queryset = super().get_queryset(request)
        return queryset.select_related('project')


class TaskInline(admin.TabularInline):
    model = Employee.tasks.through
    raw_id_fields = ('task',)


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['name', 'position']
    fields = ['name', 'position']
    inlines = [TaskInline]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['written_in', 'task']
    readonly_fields = ['written_in']

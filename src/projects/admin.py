from django.contrib import admin

from .models import Project, Task, Employee


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    pass


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    pass


class TaskInline(admin.TabularInline):
    model = Employee.tasks.through
    raw_id_fields = ('task',)


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('name', 'position')
    raw_id_fields = ('tasks',)
    inlines = [TaskInline]

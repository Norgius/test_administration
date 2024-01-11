from typing import Any
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.http import Http404

from .models import Project, Task, Employee


class MainPage(ListView):
    template_name = 'index.html'
    context_object_name = 'projects'
    extra_context = {'title': 'Главная страница'}

    def get_queryset(self) -> QuerySet[Any]:
        return Project.objects.prefetch_related('tasks').all()


class TaskDelails(DetailView):
    template_name = 'task_details.html'
    context_object_name = 'task'
    pk_url_kwarg = 'pk'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = f'Задача: {context.get("task").name}'
        return context

    def get_object(self, queryset: QuerySet[Any] | None = ...) -> Model | None:
        obj = Task.objects.get_all_joins().filter(id=self.kwargs[self.pk_url_kwarg]).first()
        if not obj:
            raise Http404
        return obj

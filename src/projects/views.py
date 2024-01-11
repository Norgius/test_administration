from typing import Any

from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, DetailView, View
from django.http.request import HttpRequest
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse

from .models import Project, Task, Comment
from .forms import CommentForm


class MainPage(ListView):
    template_name = 'index.html'
    context_object_name = 'projects'
    paginate_by = 100
    allow_empty = False
    extra_context = {'title': 'Главная страница'}

    def get_queryset(self) -> QuerySet[Any]:
        project_filter = self.request.GET.get('is_active')
        return Project.objects.filter_projects(project_filter).prefetch_related('tasks')

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        projects_filter = [
            ['?', 'Все проекты'],
            ['?is_active=1', 'Активные'],
            ['?is_active=0', 'Не активные'],
        ]
        context['projects_filter'] = projects_filter
        return context


class TaskDelails(DetailView):
    template_name = 'task_details.html'
    context_object_name = 'task'
    pk_url_kwarg = 'pk'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = f'Задача: {context.get("task").name}'
        context['form'] = CommentForm()
        return context

    def get_object(self, queryset: QuerySet[Any] | None = ...) -> Model | None:
        obj = Task.objects.get_all_joins().filter(id=self.kwargs[self.pk_url_kwarg]).first()
        if not obj:
            raise Http404
        return obj


class AddComment(View):
    def post(self, request: HttpRequest, pk: int) -> HttpResponseRedirect:
        form = CommentForm(request.POST)
        task = get_object_or_404(Task, id=pk)
        if form.is_valid():
            Comment.objects.create(**form.cleaned_data, task=task)
            return redirect(reverse('projects:task_details', kwargs={'pk': pk}))

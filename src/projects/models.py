from django.db import models
from django.urls import reverse


class ProjectQuerySet(models.QuerySet):
    def filter_projects(self, flag: str | None) -> models.QuerySet:
        match flag:
            case '1':
                return self.filter(is_active=True)
            case '0':
                return self.filter(is_active=False)
            case _:
                return self


class Project(models.Model):
    name = models.CharField('Название', max_length=255, db_index=True)
    description = models.TextField('Описание')
    is_active = models.BooleanField('Активен?', default=True)

    objects = ProjectQuerySet.as_manager()

    def __str__(self) -> str:
        return f'{self.name} - активен?: {self.is_active}'

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'

    def get_absolute_url(self):
        return reverse('projects:main_page')


class TaskQuerySet(models.QuerySet):
    def get_all_joins(self):
        return self.prefetch_related('comments', 'employees').select_related('project')


class Task(models.Model):

    class TaskStatus(models.TextChoices):
        NEW = 'NEW', 'Новая'
        IN_PROCESS = 'IN_PROCESS', 'В работе'
        CLOSED = 'CLOSED', 'Закрыта'

    name = models.CharField('Название', max_length=255, db_index=True)
    deadline = models.DateField('Срок исполнения')
    description = models.TextField('Описание')
    status = models.CharField(
        'Статус задачи',
        max_length=20,
        choices=TaskStatus.choices,
        default=TaskStatus.NEW,
        db_index=True,
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='tasks',
        verbose_name='Проект',
    )

    objects = TaskQuerySet.as_manager()

    def __str__(self) -> str:
        return f'{self.name} - {self.deadline}'

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'

    def get_absolute_url(self):
        return reverse('projects:task_details', kwargs={'pk': self.id})


class Employee(models.Model):
    name = models.CharField('ФИО сотрудника', max_length=255)
    position = models.CharField('Должность', max_length=255)
    tasks = models.ManyToManyField(
        Task,
        related_name='employees',
        verbose_name='Задачи',
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'


class Comment(models.Model):
    text = models.TextField('Tекст')
    written_in = models.DateTimeField('Дата написания', auto_now_add=True)
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Задача',
    )

    def __str__(self) -> str:
        return f'Написан в {self.written_in}'

    class Meta:
        ordering = ['-written_in']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

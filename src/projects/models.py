from django.db import models


class Project(models.Model):
    name = models.CharField('Название', max_length=255, db_index=True)
    description = models.TextField('Описание')
    is_active = models.BooleanField('Активен?', default=True)

    def __str__(self) -> str:
        return f'{self.name} - активен?: {self.is_active}'

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'


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

    def __str__(self) -> str:
        return f'{self.name} - {self.deadline}'

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'


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

from datetime import datetime
from random import choice, choices
from itertools import chain

from django.core.management.base import BaseCommand
from projects.models import Project, Task, Employee
from django.conf import settings

base_dir = settings.BASE_DIR


def create_tasks(
        words: list[str],
        sentences: list[str],
        date: datetime,
        projects: list[Project],
        task_status: Task.TaskStatus,
) -> list[Task]:
    tasks = [
        Task(
            name=choice(words),
            description=choice(sentences),
            deadline=date,
            project=choice(projects),
            status=task_status,
        )
        for _ in range(150)
    ]
    tasks = Task.objects.bulk_create(tasks)
    return tasks


class Command(BaseCommand):
    help = 'Populate DB with data'

    def add_arguments(self, parser):
        parser.add_argument('--multiplier', type=int, default=1, help='Data multiplier')
        parser.add_argument('--fio', type=str, default=base_dir / 'testdata' / 'fio.txt', help='File path')
        parser.add_argument('--positions', type=str, default=base_dir / 'testdata' / 'positions.txt', help='File path')
        parser.add_argument('--sentences', type=str, default=base_dir / 'testdata' / 'sentences.txt', help='File path')
        parser.add_argument('--words', type=str, default=base_dir / 'testdata' / 'words.txt', help='File path')
        parser.add_argument('--deadline', type=str, default='31-12-2024',
                            help='Deadline for task "day-month-year"-"30-01-2024"'
                            )

    def handle(self, *args, **kwargs):

        fio = kwargs.get('fio')
        positions = kwargs.get('positions')
        sentences = kwargs.get('sentences')
        words = kwargs.get('words')
        multiplier = kwargs.get('multiplier')
        date = datetime.strptime(kwargs.get('deadline'), '%d-%m-%Y').date()

        try:
            with open(words, 'r') as w, open(sentences, 'r') as s:
                sentences = s.readlines()
                words = w.readlines()
            with open(positions, 'r') as p, open(fio, 'r') as f:
                positions = p.readlines()
                fio = f.readlines()
        except FileNotFoundError as e:
            print(f'{e.strerror}: {e.filename}')
            exit()

        for _ in range(multiplier):

            active_projects = [
                Project(
                    name=choice(words),
                    description=choice(sentences),
                )
                for _ in range(25)
            ]

            not_active_projects = [
                Project(
                    name=choice(words),
                    description=choice(sentences),
                    is_active=False,
                )
                for _ in range(15)
            ]

            active_projects = Project.objects.bulk_create(active_projects)
            not_active_projects = Project.objects.bulk_create(not_active_projects)

            _ = create_tasks(words, sentences, date, active_projects, Task.TaskStatus.NEW)
            tasks_in_process = create_tasks(words, sentences, date, active_projects, Task.TaskStatus.IN_PROCESS)
            closed_tasks = create_tasks(words, sentences, date, not_active_projects, Task.TaskStatus.CLOSED)

            task_for_employees = list(chain(tasks_in_process, closed_tasks))

            employees = [
                Employee(
                    name=choice(fio),
                    position=choice(positions),
                )
                for _ in range(30)
            ]
            employees = Employee.objects.bulk_create(employees)
            for employee in employees:
                employee.tasks.set(choices(task_for_employees, k=30))

        print('Данные успешно добавлены')

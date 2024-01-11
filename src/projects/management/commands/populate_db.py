from datetime import datetime
from random import choice, choices

from django.core.management.base import BaseCommand
from projects.models import Project, Task, Employee
from django.conf import settings

base_dir = settings.BASE_DIR


class Command(BaseCommand):
    help = 'Populate DB with data'

    def add_arguments(self, parser):
        parser.add_argument('--multiplier', type=int, default=1, help='Data multiplier')
        parser.add_argument('--fio', type=str, default=base_dir / 'testdata' / 'fio.txt', help='File path')
        parser.add_argument('--positions', type=str, default=base_dir / 'testdata' / 'positions.txt', help='File path')
        parser.add_argument('--sentences', type=str, default=base_dir / 'testdata' / 'sentences.txt', help='File path')
        parser.add_argument('--words', type=str, default=base_dir / 'testdata' / 'words.txt', help='File path')
        parser.add_argument('--deadline', type=str, help='Deadline for task "day-month-year"-"30-01-2024"')

    def handle(self, *args, **kwargs):

        # Project.objects.all().delete()
        # Task.objects.all().delete()
        # Employee.objects.all().delete()
        fio = kwargs.get('fio')
        positions = kwargs.get('positions')
        sentences = kwargs.get('sentences')
        words = kwargs.get('words')
        multiplier = kwargs.get('multiplier')
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
            projects = [
                Project(
                    name=choice(words),
                    description=choice(sentences)
                )
                for _ in range(25)
            ]
            date = datetime.strptime(kwargs.get('deadline'), '%d-%m-%Y').date()
            projects = Project.objects.bulk_create(projects)
            tasks = [
                Task(
                    name=choice(words),
                    description=choice(sentences),
                    deadline=date,
                    project=choice(projects),
                )
                for _ in range(300)
            ]
            tasks = Task.objects.bulk_create(tasks)

            employees = [
                Employee(
                    name=choice(fio),
                    position=choice(positions),
                )
                for _ in range(25)
            ]
            employees = Employee.objects.bulk_create(employees)
            for employee in employees:
                employee.tasks.set(choices(tasks, k=25))

        print('Данные успешно добавлены')

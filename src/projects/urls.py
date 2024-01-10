from django.urls import path

from .views import MainPage, TaskDelails

app_name = 'projects'

urlpatterns = [
    path('', MainPage.as_view(), name='main_page'),
    path('task/<pk>/', TaskDelails.as_view(), name='task_details'),
]

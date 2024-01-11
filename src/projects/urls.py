from django.urls import path

from .views import MainPage, TaskDelails, AddComment

app_name = 'projects'

urlpatterns = [
    path('', MainPage.as_view(), name='main_page'),
    path('task/<pk>/', TaskDelails.as_view(), name='task_details'),
    path('task/<pk>/comment/', AddComment.as_view(), name='add_comment'),
]

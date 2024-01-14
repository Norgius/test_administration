from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

from .views import (ProjectListAPI, ProjectDetailsAPI, TaskDetailsAPI, TaskListAPI,
                    EmployeeListAPI, EmployeeDetailsAPI, EmployeeUpdateAPI, CommentAPI)

router = DefaultRouter()
router.register(r'projects', ProjectListAPI)
router.register(r'projects', ProjectDetailsAPI)
router.register(r'tasks', TaskListAPI)
router.register(r'tasks', TaskDetailsAPI)
router.register(r'employees', EmployeeListAPI)
router.register(r'employees', EmployeeDetailsAPI)
router.register(r'employees-up', EmployeeUpdateAPI)
router.register(r'comment', CommentAPI)

urlpatterns = [
    re_path(r'^auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),

    # YOUR PATTERNS
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('schema/doc/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
] + router.urls

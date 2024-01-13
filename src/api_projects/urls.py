from django.urls import path, include
from rest_framework.authtoken import views
from rest_framework.routers import SimpleRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView


from .views import ProjectAPIList, ProjectAPIDetailView
# from .views import ProjectViewSet

# router = SimpleRouter()
# router.register(r'project', ProjectViewSet)

urlpatterns = [
    path('token-auth/', views.obtain_auth_token),
    path('auth/', include('rest_framework.urls')),
    # path('', include(router.urls)),
    path('project/', ProjectAPIList.as_view()),
    # path('project-list/<int:pk>/', ProjectAPIUpdate.as_view()),
    path('project/<int:pk>/', ProjectAPIDetailView.as_view()),

    # YOUR PATTERNS
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('schema/doc/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

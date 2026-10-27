from django.contrib import admin
from django.urls import path, include
from debug_toolbar.toolbar import debug_toolbar_urls
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Cammuac - Cat Paw Destiny API",
      default_version='v1',
      description="Cammuac - Cat Paw Destiny API Documentation",
      terms_of_service="",
      contact=openapi.Contact(email="support@cammuac.com"),
      license=openapi.License(name=""),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api/v1/auth/', include('accounts.urls')),
    path('api/v1/daily-check-in/', include('activities.urls')),
    path('api/v1/diary/', include('diary.urls')),
    path('api/v1/tarot/', include('tarot.urls')),
    path('api/v1/letters/', include('letters.urls')),
] + debug_toolbar_urls()

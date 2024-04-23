from django.contrib import admin
from django.urls import include, path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.urls import re_path as url

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls', namespace='api')),
]

schema_view = get_schema_view(
   openapi.Info(
      title="Referal-system API",
      default_version='v1',
      description="Документация для приложения Referal-system.",
      contact=openapi.Contact(email="a.a.lobachev@mail.ru"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns += [
   url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0),
       name='schema-redoc'),
]

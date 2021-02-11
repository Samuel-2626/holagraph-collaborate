""" holagraph_collaborative_module URL Configuration """

# third party
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# django Apps
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static


schema_view = get_schema_view(
   openapi.Info(
      title="Collaborate API",
      default_version='v1',
      description="A Web API for collaborating with others on Holograph Web Platform",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.IsAuthenticated],
)





urlpatterns = [

    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path("ckeditor/", include('ckeditor_uploader.urls')),

    # Django admin

    path('admin/', admin.site.urls),

    # Local apps
    
    path('collaborate/api/v1/', include('api.urls')),
    path('accounts/', include('rest_auth.urls')),
    path('registration/', include('rest_auth.registration.urls')),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)





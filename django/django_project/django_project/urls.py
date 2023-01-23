from django.contrib import admin
from django.urls import path, re_path
from students import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^api/students/$', views.students_list),
    re_path(r'^api/students/(\d+)$', views.students_detail),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('blogapp/', include('blogapp.urls', namespace='blogapp')),
]

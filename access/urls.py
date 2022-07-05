from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include

admin.site.site_header = 'VACS admin'
admin.site.site_title = 'VACS admin'
admin.site.index_title = 'VACS administration'

urlpatterns = [
    path('', include("visitor.urls")),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
]

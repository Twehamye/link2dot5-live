
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('link2dot5_app.urls')),
    path('loan/', include('loans_app.urls')),
]

# config Admin Page
admin.site.site_header = "LINK2DOT5 PANEL"
admin.site.site_title = "LINK2DOT5 WEBSITE"
admin.site.index_title = "Welcome To The Administration Area" 
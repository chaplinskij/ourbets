from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.views import login, logout
from base.views import HomeView, SettingsView,  password


urlpatterns = [
   url(r'^$', HomeView.as_view(), name='home'),
   url(r'^login/$', login, name='login'),
   url(r'^logout/$', logout, name='logout'),
   url(r'^oauth/', include('social_django.urls', namespace='social')),
   url(r'^admin/', admin.site.urls),
   url(r'^settings/$', SettingsView.as_view(), name='settings'),
   url(r'^settings/password/$', password, name='password'),
]

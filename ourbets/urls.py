from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.views import login, logout
from base.views import HomeView, SettingsView,  password, ProfileView, LiveScoreView


urlpatterns = [
   url(r'^$', HomeView.as_view(), name='home'),
   url(r'^live/$', LiveScoreView.as_view(), name='livescore'),
   url(r'^login/$', login, name='login'),
   url(r'^logout/$', logout, name='logout'),
   url(r'^oauth/', include('social_django.urls', namespace='social')),
   url(r'^admin/', admin.site.urls),
   url(r'^settings/$', SettingsView.as_view(), name='settings'),
   url(r'^settings/password/$', password, name='password'),
   url(r'^profile/$', ProfileView.as_view(), name='profile'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

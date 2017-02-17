
from django.views.generic import RedirectView
from django.conf.urls import url


urlpatterns = [
   url(r'^mbb/$', F.as_view(), name='article-mbb'),
]
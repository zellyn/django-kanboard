from django.conf.urls.defaults import *
# The next two lines enable the admin and load each admin.py file:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/(.*)', admin.site.root),
    (r'^kanboard/', include('kanboard.urls')),
)

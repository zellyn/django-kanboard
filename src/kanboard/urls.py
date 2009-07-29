import os
from django.conf.urls.defaults import patterns, url
import kanboard

urlpatterns = patterns('kanboard.views',
   url(r'^board/(?P<board_slug>[\w-]+)/$', 'board'),
   url(r'^board/(?P<board_slug>[\w-]+)/update/$', 'update'),
)

# Serve static content
static_root = os.path.join(os.path.dirname(kanboard.__file__), 'static')
urlpatterns += patterns('',
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': static_root})
)

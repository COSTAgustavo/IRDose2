from django.urls import re_path as url

from .views import (
     IRDoseListView,
     IRDoseDetailView,
     IRDoseCreateView,
     IRDoseUpdateView
)
app_name = "IRDoseApp"
urlpatterns = [
    url(r'^create/$', IRDoseCreateView.as_view(), name='create'),
    url(r'^(?P<slug>[\w-]+)/$', IRDoseDetailView.as_view(), name='infos'),
    url(r'^(?P<slug>[\w-]+)/edit/$', IRDoseUpdateView.as_view(), name='edit'),
    url(r'$', IRDoseListView.as_view(), name='IRDoseApp'),
]

# channel_routing = [
#     route("websocket.connect", websocket_connect),
#     route("websocket.receive", websocket_receive),
#     route("websocket.disconnect", websocket_disconnect),
#     route("my-background-task", my_background_task),
# ]
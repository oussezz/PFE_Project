from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import path,include

from .views import *

urlpatterns = [
    path('myaccount/', myaccount, name="myaccount"),
    path("admins/", admins, name="admins"),
    path("users/", users, name="users"),
    path("delete_user/<int:id>", delete_user, name="delete_user"),
    path('live_camera/<int:id>', live_camera, name="live_camera"),
    path('activate_camera', activate_camera, name="activate_camera"),
    path('view_camera/<int:id>',view_camera,name="view_camera"),
    path(("streaming_server_cameras"), streaming_server_cameras, name="streaming_server_cameras"),
    path(("add_camera"), add_camera, name="add_camera"),
    path(("delete_camera/<int:id>"), delete_camera, name="delete_camera"),
    path("stop_thread", stop_thread, name="stop_thread"),
    path("firedetection", firedetection, name="firedetection"),
    path("map", map, name="map"),
    path('', home, name='home'),
    path('stop', stop, name='stop'),
    path('history', history, name='history'),
    path('cam_history/<int:id>', cam_history, name='cam_history'),
    path('reports',reports, name='reports'),
    path('stats',stats,name="stats"),
    path('logs',logs,name="logs"),
    path('mark_notification_as_read/<int:id>',mark_notification_as_read,name="mark_notification_as_read"),
    path('update_notifications',update_notifications,name="update_notifications"),
    path("clientcameras", clientcameras, name="clientcameras"),
    path('live_camera_ajax/<int:id>', live_camera_ajax, name="live_camera_ajax"),
    
]
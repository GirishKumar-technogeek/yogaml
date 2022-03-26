from django.urls import path
from . import views

urlpatterns = [
    path('view_poses/',views.view_poses,name='admin_view_poses'),
    path('add_pose/',views.add_pose,name='add_pose'),
]
from django.urls import path
from . import views

urlpatterns = [
    path('view_profile/',views.view_profile,name='view_profile'),
    path('add_profile/',views.add_profile,name='add_profile'),
    path('search_poses/',views.search_poses,name='search_poses'),
    path('view_poses/',views.view_poses,name='view_poses'),
    path('view_pose/<int:pk>',views.view_pose,name='view_pose'),
    path('score_user/<int:pk>',views.score_user,name='score_user'),
    path('my_progress/',views.my_progress,name='my_progress'),
    path('leaderboard/',views.leaderboard,name='leaderboard'),
]
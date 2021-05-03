from .import views
from django.urls import path

urlpatterns = [
    path('', views.home, name='home'),
    path('video/<int:pk>/', views.video, name='video'),
    path('search/', views.search, name='search'),
    path('channel/<int:pk>/', views.channel, name='channel'),
    path('upload/', views.upload, name='upload'),
    path('handleSignup/', views.handleSignup, name='handleSignup'),
    path('handleLogin/', views.handleLogin, name='handleLogin'),
    path('handleLogout/', views.handleLogout, name='handleLogout'),
    path('like-video/<int:pk>/', views.likeVideo, name='likeVideo'),
    path('cancel-like/<int:pk>/', views.cancelLike, name='cancelLike'),
    path('dislike-video/<int:pk>/', views.dislikeVideo, name='dislikeVideo'),
    path('cancel-dislike/<int:pk>/', views.cancelDislike, name='cancelDislike'),
    path('subscribe/<int:pk>/', views.subscribe, name='subscribe'),
    path('comment/<int:pk>/', views.comment, name='comment'),
    path('upload-video/', views.uploadVideo, name='uploadVideo'),
    path('more-comments/<int:pk>/', views.moreComments, name='moreComments'),
]


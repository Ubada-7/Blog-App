from django.urls import path , include

from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('Signup', views.Signup, name='Signup'),
    path('Signin', views.Signin, name='Signin'),
    path('SignOut', views.SignOut, name='SignOut'),
    path('create_blog',views.create_blog, name='create_blog'),
    path('blog_list/',views.blog_list, name='blog_list'), # Define the URL pattern
    path('like_post/<int:post_id>/', views.LikeView.as_view(), name='like_post'),
    path('add_comment/<int:post_id>/', views.add_comment, name='add_comment'),
    path('check_like/<int:post_id>/', views.CheckLikeView.as_view(), name='check_like'),
    path('like_comment/<int:comment_id>/', views.like_comment, name='like_comment'),
    path('add_reply/<int:comment_id>/', views.add_reply, name='add_reply'),
    path('get_replies/<int:comment_id>/', views.get_replies, name='get_replies'),
    path('approve_blog/<int:blog_id>/', views.approve_blog, name='approve_blog'),
    path('reject_blog/<int:blog_id>/', views.reject_blog, name='reject_blog'),
    path('moderator_dashboard', views.moderator_dashboard, name='moderator_dashboard'),
    path('report_post/<int:post_id>/', views.report_post, name='report_post'),
    path('handle_reports/', views.handle_reports, name='handle_reports'),


]


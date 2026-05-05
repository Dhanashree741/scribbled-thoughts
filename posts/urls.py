from django.urls import path
from . import views

urlpatterns = [
    path('',views.index, name='index'),
    path('post/<int:pk>',views.post, name='post'),
    path('category/<int:id>',views.category_posts,name='category_posts'),
    path('signup/',views.signup,name='signup'),
    path('login/',views.user_login,name='login'),
    path('logout/',views.user_logout,name='logout'),
    path('add_comment/<int:id>/', views.add_comment, name='add_comment'),
    path('like/<int:id>/', views.like_post, name='like_post'),
]
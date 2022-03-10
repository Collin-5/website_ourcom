from django.urls import path
from .views import PostView, post_detail, add_post ,update_post, delete_post, update_comment, delete_comment

app_name = 'posts'
urlpatterns = [
    path('<int:id>/<int:id1>/delete', delete_comment, name='delete_comment'),
    path('<int:id>/<int:id1>/update', update_comment, name='update_comment'),
    path('<int:id>/delete', delete_post, name='delete_post'),
    path('<int:id>', update_post, name='update_post'),
    path('add_post', add_post, name='add_post'),
    path('', PostView, name='allposts'),
    path('<int:id>/', post_detail, name='post_details')
]

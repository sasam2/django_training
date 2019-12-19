from django.conf.urls import url, include
from . import views

urlpatterns = [
    url('post_view', views.post_view, name='post_view'),
    url('post_create', views.post_create, name='post_create'),
    url('post_delete', views.post_delete, name='post_delete'),
    url('signup', views.signup, name='signup'),
    url('signin', views.signin, name='signin'),
    url('signout', views.signout, name='signout')
]
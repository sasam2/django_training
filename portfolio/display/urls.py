from django.conf.urls import url, include
from . import views

urlpatterns = [
    url('post_show', views.post_show, name='post_show'),
    url('post_new', views.post_new, name='post_new'),
    url('signup', views.signup, name='signup'),
    url('signin', views.signin, name='signin'),
    url('signout', views.signout, name='signout')
]
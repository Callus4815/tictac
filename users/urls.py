from django.conf.urls import url, include
from . import views as users_views

urlpatterns = [
    url(r'^home$', users_views.home, name='users_home'),

]

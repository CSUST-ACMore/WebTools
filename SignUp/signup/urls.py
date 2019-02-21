
from django.conf.urls import url
from django.template.context_processors import static

from SignUp import settings
from . import views

app_name = 'signup'
urlpatterns = [
    url(r'^index', views.index, name='index'),
    url(r'^register', views.register, name='register'),
    url(r'^list', views.par_list, name='list'),
    url(r'^lottery', views.lottery, name='lottery'),
    url(r'^scrollboard', views.scrollboard, name='scrollboard'),
    url(r'^$', views.index, name='index')
]

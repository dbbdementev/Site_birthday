import django.conf.urls

from . import views

app_name = 'register_activate'
urlpatterns = [
    django.conf.urls.url(r'^$', views.mainpage, name='mainpage'),
    django.conf.urls.url(r'^signup/$', views.register, name='signup'),
    django.conf.urls.url(r'^activation/', views.activate, name='activation'),
    django.conf.urls.url(r'^signin/$', views.log_in, name='signin'),
    django.conf.urls.url(r'^logout/$', views.log_out, name='logout'),
    django.conf.urls.url(r'^register_vk/$', views.register_vk, name='register_vk'),
    django.conf.urls.url(r'^register_ok/$', views.register_ok, name='register_ok'),
    django.conf.urls.url(r'^register_f/$', views.register_f, name='register_f'),
    django.conf.urls.url(r'^contacts/', views.contacts, name='contacts'),

]

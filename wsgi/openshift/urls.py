from django.conf.urls import patterns, include, url
from django.contrib import admin
import views

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    # ex: /zohar/5/
    #url(r'^(?P<book_number>\d+)/$', views.book, name='view_book'),
)
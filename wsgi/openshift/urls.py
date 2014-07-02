from django.conf.urls import patterns, include, url
import views
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    #url(r'^$', 'views.home', name='home'),
    url(r'^$', views.index, name='index'),
    # ex: /zohar/5/
    url(r'^(?P<book_number>\d+)/$', views.book, name='view_book'),

    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

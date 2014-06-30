from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'views.home', name='home'),
    url(r'^zohar/', 'views.index', name='index'),
    # ex: /zohar/5/
    url(r'^(?P<book_number>\d+)/$', 'views.book', name='view_book'),

    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

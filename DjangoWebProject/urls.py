"""
Definition of urls for DjangoWebProject.
"""

from datetime import datetime
from django.conf.urls import patterns, url
from app.forms import BootstrapAuthenticationForm

urlpatterns = patterns('',
    url(r'^$', 'app.views.home', name='home'),
    url(r'^searchFilers$', 'app.views.filters', name='searchFilters'),
    url(r'^doSearch/(?P<fieldID>\d+)/(?P<gradeID>\d+)/(?P<provID>\d+)/(?P<ageID>\d+)/(?P<genderID>\d+)$', 'app.views.search', name='doSearch'),
    url(r'^contact$', 'app.views.contact', name='contact'),
    url(r'^about$', 'app.views.about', name='about'),
)

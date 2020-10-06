from django.conf.urls import url

from .views import (
        InsuranceplanListView,
        InsuranceplanDetailSlugView,
        InsuranceplanDownloadView
        )

urlpatterns = [
    url(r'^$', InsuranceplanListView.as_view(), name='list'),
    url(r'^(?P<slug>[\w-]+)/$', InsuranceplanDetailSlugView.as_view(), name='detail'),
    url(r'^(?P<slug>[\w-]+)/(?P<pk>\d+)/$', InsuranceplanDownloadView.as_view(), name='download'),
]
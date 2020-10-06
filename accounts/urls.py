from django.conf.urls import url

from insuranceplans.views import UserInsuranceplanHistoryView
from .views import (
    AccountHomeView,
    AccountEmailActivateView,
    UserDetailUpdateView
)

urlpatterns = [
    url(r'^$', AccountHomeView.as_view(), name='home'),
    url(r'^details/$', UserDetailUpdateView.as_view(), name='user-update'),
    url(r'^history/insuranceplans/$', UserInsuranceplanHistoryView.as_view(), name='user-insuranceplan-history'),
    url(r'^email/confirm/(?P<key>[0-9A-Za-z]+)/$', AccountEmailActivateView.as_view(), name='email-activate'),
    url(r'^email/resend-activation/$', AccountEmailActivateView.as_view(), name='resend-activation'),
]

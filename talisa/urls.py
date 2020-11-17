"""talisa URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path, include, re_path
from django.views.generic import RedirectView, TemplateView

from accounts.views import LoginView, GuestRegisterView, RegisterView
from addresses.views import AddressListView, AddressCreateView, AddressUpdateView, checkout_address_create_view, \
    checkout_address_reuse_view
from analytics.views import SalesView, SalesAjaxView
from billing.views import payment_method_view, payment_method_createview
from carts.views import cart_detail_api_view
from marketing.views import MarketingPreferenceUpdateView, MailchimpWebhookView
from orders.views import LibraryView
from talisa.views import home_page, about_page, contact_page


urlpatterns = [
    path('', home_page, name='home'),
    path('about/', about_page, name='about'),
    path('articles/', include(('articles.urls', 'articles'), namespace='articles')),

    path('accounts/', RedirectView.as_view(url='/account')),
    path('account/', include(('accounts.urls', 'account'), namespace='account')),
    path('accounts/', include("accounts.passwords.urls")),
    path('admin-Talisa-Ng/', admin.site.urls),

    path('login/', LoginView.as_view(), name='login'),
    path('register/guest/', GuestRegisterView.as_view(), name='guest_register'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    
    url(r'^address/$', RedirectView.as_view(url='/addresses')),
    url(r'^addresses/$', AddressListView.as_view(), name='addresses'),
    url(r'^addresses/create/$', AddressCreateView.as_view(), name='address-create'),
    url(r'^addresses/(?P<pk>\d+)/$', AddressUpdateView.as_view(), name='address-update'),
    url(r'^analytics/sales/$', SalesView.as_view(), name='sales-analytics'),
    url(r'^analytics/sales/data/$', SalesAjaxView.as_view(), name='sales-analytics-data'),
    url(r'^contact/$', contact_page, name='contact'),
    url(r'^checkout/address/create/$', checkout_address_create_view, name='checkout_address_create'),
    url(r'^checkout/address/reuse/$', checkout_address_reuse_view, name='checkout_address_reuse'),
    url(r'^api/cart/$', cart_detail_api_view, name='api-cart'),
    url(r'^cart/', include(("carts.urls", 'cart'), namespace='cart')),
    url(r'^billing/payment-method/$', payment_method_view, name='billing-payment-method'),
    url(r'^billing/payment-method/create/$', payment_method_createview, name='billing-payment-method-endpoint'),
    url(r'^bootstrap/$', TemplateView.as_view(template_name='bootstrap/example.html')),
    url(r'^library/$', LibraryView.as_view(), name='library'),
    url(r'^orders/', include(("orders.urls", 'orders'), namespace='orders')),
    url(r'^insuranceplans/', include(("insuranceplans.urls", 'insuranceplans'), namespace='insuranceplans')),
    # url(r'^search/', include("search.urls", namespace='search')),
    url(r'^settings/$', RedirectView.as_view(url='/account')),
    url(r'^settings/email/$', MarketingPreferenceUpdateView.as_view(), name='marketing-pref'),
    url(r'^webhooks/mailchimp/$', MailchimpWebhookView.as_view(), name='webhooks-mailchimp'),
]

# administrator backend service url
# urlpatterns += [
#     path('admin-Talisa-Ng/', admin.site.urls),
# ]

# url to catch any unmatch url for 404...
urlpatterns += [re_path(r'^.*', TemplateView.as_view(template_name='404.html'))]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
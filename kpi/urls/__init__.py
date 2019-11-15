# coding: utf-8
import private_storage.urls
from django.contrib.auth import logout
from django.urls import include, re_path
from django.views.i18n import JavaScriptCatalog

from hub.models import ConfigurationFile
from hub.views import ExtraDetailRegistrationView
from kobo.apps.superuser_stats.views import user_report, retrieve_user_report
from kpi.forms import RegistrationForm
from kpi.views import authorized_application_authenticate_user
from kpi.views import home, one_time_login, browser_tests
from kpi.views.environment import EnvironmentView
from kpi.views.current_user import CurrentUserViewSet
from kpi.views.token import TokenView

from .router_api_v1 import router_api_v1
from .router_api_v2 import router_api_v2, URL_NAMESPACE

# TODO: Give other apps their own `urls.py` files instead of importing their
# views directly! See
# https://docs.djangoproject.com/en/1.8/intro/tutorial03/#namespacing-url-names


# Apps whose translations should be available in the client code.
js_info_dict = {
    'packages': ('kobo.apps.KpiConfig',),
}

urlpatterns = [
    re_path(r'^$', home, name='kpi-root'),
    re_path(r'^me/$', CurrentUserViewSet.as_view({
        'get': 'retrieve',
        'patch': 'partial_update',
    }), name='currentuser-detail'),
    re_path(r'^', include(router_api_v1.urls)),
    re_path(r'^api/v2/', include((router_api_v2.urls, URL_NAMESPACE))),
    re_path(r'^api-auth/', include('rest_framework.urls',
                                   namespace='rest_framework')),
    re_path(r'^accounts/register/$', ExtraDetailRegistrationView.as_view(
        form_class=RegistrationForm), name='registration_register'),
    re_path(r'^accounts/logout/', logout, {'next_page': '/'}),
    re_path(r'^accounts/', include('registration.backends.default.urls')),
    re_path(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    re_path(
        r'^authorized_application/authenticate_user/$',
        authorized_application_authenticate_user
    ),
    re_path(r'^browser_tests/$', browser_tests),
    re_path(r'^authorized_application/one_time_login/$', one_time_login),
    re_path(r'^i18n/', include('django.conf.urls.i18n')),
    # Translation catalog for client code.
    re_path(r'^jsi18n/$', JavaScriptCatalog, js_info_dict, name='javascript-catalog'),

    re_path(r'^token/$', TokenView.as_view(), name='token'),
    re_path(r'^environment/$', EnvironmentView.as_view(), name='environment'),
    re_path(r'^configurationfile/(?P<slug>[^/]+)/?',
            ConfigurationFile.redirect_view, name='configurationfile'),
    re_path(r'^private-media/', include(private_storage.urls)),
    # Statistics for superusers
    re_path(r'^superuser_stats/user_report/$', user_report),
    re_path(r'^superuser_stats/user_report/(?P<base_filename>[^/]+)$',
            retrieve_user_report),
]

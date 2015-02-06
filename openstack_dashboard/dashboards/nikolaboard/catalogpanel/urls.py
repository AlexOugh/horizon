from django.conf.urls import patterns
from django.conf.urls import url

from openstack_dashboard.dashboards.nikolaboard.catalogpanel import views


urlpatterns = patterns(
    '',
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^\?tab=catalogpanel_tabs__tab$', views.IndexView.as_view(), name='catalogpanel_tabs'),
)

from django.conf.urls import patterns
from django.conf.urls import url

from openstack_dashboard.dashboards.nikolaboard.workflowpanel import views

urlpatterns = patterns(
    '',
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^\?tab=workflowpanel_tabs_tab$', views.IndexView.as_view(), name='workflowpanel_tabs'),
)

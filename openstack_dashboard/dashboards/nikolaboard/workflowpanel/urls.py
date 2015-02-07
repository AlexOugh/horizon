from django.conf.urls import patterns
from django.conf.urls import url

from openstack_dashboard.dashboards.nikolaboard.workflowpanel import views

urlpatterns = patterns(
    '',
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^workflow/(?P<workflow_id>[^/]+)/$', views.DetailView.as_view(), name='detail'),
)

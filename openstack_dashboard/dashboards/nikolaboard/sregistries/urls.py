from django.conf.urls import patterns
from django.conf.urls import url

from openstack_dashboard.dashboards.nikolaboard.sregistries import views


urlpatterns = patterns(
    '',
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^registry/(?P<registry_id>[^/]+)/$', views.DetailView.as_view(), name='detail'),
)

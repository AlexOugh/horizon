from django.conf.urls import patterns
from django.conf.urls import url

from openstack_dashboard.dashboards.nikolaboard.iams import views


urlpatterns = patterns(
    '',
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^iam/(?P<iam_user_id>[^/]+)/$', views.DetailView.as_view(), name='detail'),
)

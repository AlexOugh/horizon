from horizon import tables
from horizon import tabs
from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from horizon import exceptions
from horizon import forms

from openstack_dashboard import api
from openstack_dashboard.dashboards.nikolaboard.iams import tables as nikolaboard_tables
from openstack_dashboard.dashboards.nikolaboard.iams import tabs as nikolaboard_tabs
#from openstack_dashboard.dashboards.nikolaboard.iams import forms as nikolaboard_forms


class IndexView(tables.DataTableView):
    table_class = nikolaboard_tables.IAMTable
    template_name = 'nikolaboard/iams/index.html'

    def __init__(self, *args, **kwargs):
        super(IndexView, self).__init__(*args, **kwargs)
        self._more = None

    def has_prev_data(self, table):
        return self._prev

    def has_more_data(self, table):
        return self._more

    def get_data(self):
        prev_marker = self.request.GET.get(nikolaboard_tables.IAMTable._meta.prev_pagination_param)
        if prev_marker is not None:
            sort_dir = 'asc'
            marker = prev_marker
        else:
            sort_dir = 'desc'
            marker = self.request.GET.get(nikolaboard_tables.IAMTable._meta.pagination_param)

        try:
            iam_users, self._more, self._prev = api.nikola.iam.list_iam_users(
                self.request,
                search_opts={'marker': marker, 'paginate': True})
            if prev_marker is not None:
                iam_users = sorted(iam_users, key=attrgetter('created_at'), reverse=True)
            return iam_users
        except Exception:
            self._prev = False
            self._more = False
            error_message = _('Unable to get iam users')
            exceptions.handle(self.request, error_message)
            return []


class DetailView(tabs.TabbedTableView):
    tab_group_class = nikolaboard_tabs.IAMTabs
    template_name = 'nikolaboard/iams/detail.html'

    def get_data(self, request, *args, **kwargs):
        iam_user_id = kwargs['iam_user_id']
        try:
            iam_user = api.nikola.iam.get_iam_user(
                request,
                iam_user_id)
            request.session['iam_user_id'] = iam_user.id
            #request.session['iam_user_name'] = iam_user.op_username
            return iam_user
        except Exception:
            msg = _("Unable to retrieve iam user.")
            print msg
            exceptions.handle(request, msg, redirect=self.get_redirect_url())


    '''#@memoized.memoized_method
    def get_template(self, request, **kwargs):
        try:
            catalog_id = kwargs['catalog_id']
            catalog_template = api.nikola.workflow.get_catalog(
                request,
                catalog_id).content
            return catalog_template
        except Exception:
            msg = _("Unable to retrieve catalog template.")
            print msg
            exceptions.handle(request, msg, redirect=self.get_redirect_url())'''


    def get_tabs(self, request, **kwargs):
        iam_user = self.get_data(request, **kwargs)
        #registry_template = registry.content
        #registry_parameters = registry.parameters
        return self.tab_group_class(
            #request, registry=registry, registry_template=registry_template, registry_parameters=registry_parameters, **kwargs)
            request, iam_user=iam_user, **kwargs)


    @staticmethod
    def get_redirect_url():
        return reverse('horizon:nikolaboard:iams:index')



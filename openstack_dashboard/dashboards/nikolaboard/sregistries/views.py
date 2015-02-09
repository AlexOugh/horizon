
from horizon import tables
from horizon import tabs
from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from horizon import exceptions
from horizon import forms

from openstack_dashboard import api
from openstack_dashboard.dashboards.nikolaboard.sregistries import tables as nikolaboard_tables
from openstack_dashboard.dashboards.nikolaboard.sregistries import tabs as nikolaboard_tabs
#from openstack_dashboard.dashboards.nikolaboard.sregistries import forms as nikolaboard_forms


class IndexView(tables.DataTableView):
    table_class = nikolaboard_tables.RegistryTable
    template_name = 'nikolaboard/sregistries/index.html'

    def __init__(self, *args, **kwargs):
        super(IndexView, self).__init__(*args, **kwargs)
        self._more = None

    def has_prev_data(self, table):
        return self._prev

    def has_more_data(self, table):
        return self._more

    def get_data(self):
        prev_marker = self.request.GET.get(nikolaboard_tables.RegistryTable._meta.prev_pagination_param)
        if prev_marker is not None:
            sort_dir = 'asc'
            marker = prev_marker
        else:
            sort_dir = 'desc'
            marker = self.request.GET.get(nikolaboard_tables.RegistryTable._meta.pagination_param)

        try:
            registries, self._more, self._prev = api.nikola.sregistry.list_registries(
                self.request,
                search_opts={'marker': marker, 'paginate': True})
            if prev_marker is not None:
                registries = sorted(registries, key=attrgetter('created_at'), reverse=True)
            return registries
        except Exception:
            self._prev = False
            self._more = False
            error_message = _('Unable to get service registries')
            exceptions.handle(self.request, error_message)
            return []


class DetailView(tabs.TabbedTableView):
    tab_group_class = nikolaboard_tabs.RegistryTabs
    template_name = 'nikolaboard/sregistries/detail.html'

    def get_data(self, request, *args, **kwargs):
        registry_id = kwargs['registry_id']
        try:
            registry = api.nikola.sregistry.get_registry(
                request,
                registry_id)
            request.session['registry_id'] = registry.id
            request.session['registry_name'] = registry.name
            return registry
        except Exception:
            msg = _("Unable to retrieve registry.")
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
        registry = self.get_data(request, **kwargs)
        #registry_template = registry.content
        #registry_parameters = registry.parameters
        return self.tab_group_class(
            #request, registry=registry, registry_template=registry_template, registry_parameters=registry_parameters, **kwargs)
            request, registry=registry, **kwargs)


    @staticmethod
    def get_redirect_url():
        return reverse('horizon:nikolaboard:sregistries:index')



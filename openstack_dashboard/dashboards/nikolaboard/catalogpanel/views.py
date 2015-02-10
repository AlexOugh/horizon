
from horizon import tables
from horizon import tabs
from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from horizon import exceptions
from horizon import forms

from openstack_dashboard import api
from openstack_dashboard.dashboards.nikolaboard.catalogpanel import tables as nikolaboard_tables
from openstack_dashboard.dashboards.nikolaboard.catalogpanel import tabs as nikolaboard_tabs
from openstack_dashboard.dashboards.nikolaboard.catalogpanel import forms as nikolaboard_forms


class IndexView(tables.DataTableView):
    table_class = nikolaboard_tables.CatalogTable
    template_name = 'nikolaboard/catalogpanel/index.html'

    def __init__(self, *args, **kwargs):
        super(IndexView, self).__init__(*args, **kwargs)
        self._more = None

    def has_prev_data(self, table):
        return self._prev

    def has_more_data(self, table):
        return self._more

    def get_data(self):
        stacks = []
        prev_marker = self.request.GET.get(nikolaboard_tables.CatalogTable._meta.prev_pagination_param)
        if prev_marker is not None:
            sort_dir = 'asc'
            marker = prev_marker
        else:
            sort_dir = 'desc'
            marker = self.request.GET.get(nikolaboard_tables.CatalogTable._meta.pagination_param)

        try:
            catalogs, self._more, self._prev = api.nikola.catalog.list_catalogs(
                self.request,
                search_opts={'marker': marker, 'paginate': True})
            if prev_marker is not None:
                workbooks = sorted(catalogs, key=attrgetter('created_at'), reverse=True)
            return catalogs
        except Exception:
            self._prev = False
            self._more = False
            error_message = _('Unable to get catalogs')
            exceptions.handle(self.request, error_message)
            return []


class DetailView(tabs.TabbedTableView):
    tab_group_class = nikolaboard_tabs.CatalogTabs
    template_name = 'nikolaboard/catalogpanel/detail.html'

    def get_data(self, request, *args, **kwargs):
        catalog_id = kwargs['catalog_id']
        try:
            catalog = api.nikola.catalog.get_catalog(
                request,
                catalog_id)
            request.session['catalog_id'] = catalog.id
            request.session['catalog_name'] = catalog.name
            return catalog
        except Exception:
            msg = _("Unable to retrieve catalog.")
            print msg
            exceptions.handle(request, msg, redirect=self.get_redirect_url())


    #@memoized.memoized_method
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
            exceptions.handle(request, msg, redirect=self.get_redirect_url())


    def get_tabs(self, request, **kwargs):
        catalog = self.get_data(request, **kwargs)
        catalog_template = catalog.content
        catalog_parameters = catalog.parameters
        return self.tab_group_class(
            request, catalog=catalog, catalog_template=catalog_template, catalog_parameters=catalog_parameters, **kwargs)


    @staticmethod
    def get_redirect_url():
        return reverse('horizon:nikolaboard:catalogpanel:index')


class LaunchCatalogView(forms.ModalFormView):
    template_name = 'nikolaboard/catalogpanel/launch.html'
    modal_header = _("Launch Service Catalog")
    form_id = "launch_catalog_form"
    form_class = nikolaboard_forms.LaunchCatalogForm
    submit_label = _("Launch Service Catalog")
    submit_url = reverse_lazy("horizon:nikolaboard:catalogpanel:launch")
    success_url = reverse_lazy('horizon:project:stacks:index')

    def dispatch(self, *args, **kwargs):
        return super(LaunchCatalogView, self).dispatch(*args, **kwargs)


    def get_form_kwargs(self):
        kwargs = super(LaunchCatalogView, self).get_form_kwargs()
        return kwargs


    def get_initial(self):
        service_catalog = self.get_object()
        return {'catalog_id': service_catalog.id, 'catalog_name':service_catalog.name, 'catalog_parameters':service_catalog.parameters}


    def get_context_data(self, **kwargs):
        context = super(LaunchCatalogView, self).get_context_data(**kwargs)
        service_catalog = self.get_object()
        context['catalog_id'] = service_catalog.id
        context['catalog_parameters'] = service_catalog.parameters
        return context


    def get_object(self):
        catalog_id = self.kwargs['catalog_id']
        try:
            service_catalog = api.nikola.catalog.get_catalog(
                self.request,
                catalog_id)
        except Exception:
            msg = _("Unable to retrieve service catalog.")
            redirect = reverse('horizon:nikolaboard:catalogpanel:index')
            exceptions.handle(self.request, msg, redirect=redirect)
        return service_catalog



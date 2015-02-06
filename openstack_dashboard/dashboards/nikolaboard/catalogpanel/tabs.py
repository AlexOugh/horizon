from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import tabs

from openstack_dashboard import api
from openstack_dashboard.dashboards.nikolaboard.catalogpanel import tables


class ServiceCatalogTab(tabs.TableTab):
    name = _("List")
    slug = "service_catalog_tab"
    table_classes = (tables.ServiceCatalogTable,)
    template_name = ("horizon/common/_detail_table.html")
    preload = False

    def has_more_data(self, table):
        return self._has_more

    def get_service_catalog_data(self):
        try:
            marker = self.request.GET.get(
                        tables.ServiceCatalogTable._meta.pagination_param, None)

            #instances, self._has_more = api.nova.server_list(
            catalogs, self._has_more, has_prev_data = api.nikola.catalog.list_catalogs(
                self.request,
                search_opts={'marker': marker, 'paginate': True})
            #return instances
            return catalogs
        except Exception:
            self._has_more = False
            error_message = _('Unable to get catalogs')
            exceptions.handle(self.request, error_message)

            return []

class CatalogpanelTabs(tabs.TabGroup):
    slug = "catalogpanel_tabs"
    tabs = (ServiceCatalogTab,)
    sticky = True

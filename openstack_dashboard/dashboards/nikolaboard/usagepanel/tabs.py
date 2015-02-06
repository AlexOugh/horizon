from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import tabs

from openstack_dashboard import api
from openstack_dashboard.dashboards.nikolaboard.usagepanel import tables


class UsageTab(tabs.TableTab):
    name = _("List")
    slug = "usage_tab"
    table_classes = (tables.UsageTable,)
    template_name = ("horizon/common/_detail_table.html")
    preload = False

    def has_more_data(self, table):
        return self._has_more

    def get_usage_data(self):
        try:
            marker = self.request.GET.get(
                        tables.UsageTable._meta.pagination_param, None)

            usages, self._has_more, has_prev_data = api.nikola.usage.list_usages(
                self.request,
                search_opts={'marker': marker, 'paginate': True})
            return usages
        except Exception:
            self._has_more = False
            error_message = _('Unable to get usages')
            exceptions.handle(self.request, error_message)

            return []

class UsagepanelTabs(tabs.TabGroup):
    slug = "usagepanel_tabs"
    tabs = (UsageTab,)
    sticky = True

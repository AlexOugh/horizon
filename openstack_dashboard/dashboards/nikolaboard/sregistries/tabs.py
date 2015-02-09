from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import tabs

from openstack_dashboard import api
from openstack_dashboard.dashboards.nikolaboard.catalogpanel import tables


class RegistryTab(tabs.Tab):
    name = _("Overview")
    slug = "service_registry_tab"
    template_name = "nikolaboard/sregistries/_registry_detail.html"
    preload = False

    def allowed(self, request):
        return True

    def get_context_data(self, request):
        return {"registry": self.tab_group.kwargs['registry']}


'''class CatalogTemplateTab(tabs.Tab):
    name = _("Template")
    slug = "catalog_template"
    template_name = "nikolaboard/catalogpanel/_catalog_template.html"

    def allowed(self, request):
        return True

    def get_context_data(self, request):
        return {"catalog_template": self.tab_group.kwargs['catalog_template']}'''


class RegistryTabs(tabs.TabGroup):
    slug = "Registrypanel_tabs"
    tabs = (RegistryTab,)
    #tabs = (RegistryTab, RegistryTemplateTab)
    sticky = True

from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import tabs

from openstack_dashboard import api
from openstack_dashboard.dashboards.nikolaboard.catalogpanel import tables


class CatalogTab(tabs.Tab):
    name = _("Overview")
    slug = "service_catalog_tab"
    template_name = "nikolaboard/catalogpanel/_catalog_detail.html"
    preload = False

    def allowed(self, request):
        #return policy.check(
        #    (("orchestration", "cloudformation:DescribeStacks"),),
        #    request)
        return True

    def get_context_data(self, request):
        return {"catalog": self.tab_group.kwargs['catalog']}


class CatalogTemplateTab(tabs.Tab):
    name = _("Template")
    slug = "catalog_template"
    template_name = "nikolaboard/catalogpanel/_catalog_template.html"

    def allowed(self, request):
        #return policy.check(
        #    (("orchestration", "cloudformation:DescribeStacks"),),
        #    request)
        return True

    def get_context_data(self, request):
        return {"catalog_template": self.tab_group.kwargs['catalog_template']}


class CatalogTabs(tabs.TabGroup):
    slug = "catalogpanel_tabs"
    tabs = (CatalogTab, CatalogTemplateTab)
    sticky = True

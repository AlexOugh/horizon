from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import tabs

from openstack_dashboard import api
from openstack_dashboard.dashboards.nikolaboard.iams import tables


class IAMTab(tabs.Tab):
    name = _("Overview")
    slug = "iam_tab"
    template_name = "nikolaboard/iams/_iam_detail.html"
    preload = False

    def allowed(self, request):
        return True

    def get_context_data(self, request):
        return {"iam_user": self.tab_group.kwargs['iam_user']}


'''class CatalogTemplateTab(tabs.Tab):
    name = _("Template")
    slug = "catalog_template"
    template_name = "nikolaboard/catalogpanel/_catalog_template.html"

    def allowed(self, request):
        return True

    def get_context_data(self, request):
        return {"catalog_template": self.tab_group.kwargs['catalog_template']}'''


class IAMTabs(tabs.TabGroup):
    slug = "IAM_tabs"
    tabs = (IAMTab,)
    #tabs = (IAMTab, RegistryTemplateTab)
    sticky = True

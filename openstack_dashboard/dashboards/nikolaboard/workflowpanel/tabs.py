from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import tabs

from openstack_dashboard import api
from openstack_dashboard.dashboards.nikolaboard.workflowpanel import tables


class WorkflowTab(tabs.Tab):
    name = _("Overview")
    slug = "workflow_tab"
    template_name = "nikolaboard/workflowpanel/_workflow_detail.html"
    preload = False

    def allowed(self, request):
        #return policy.check(
        #    (("orchestration", "cloudformation:DescribeStacks"),),
        #    request)
        return True

    def get_context_data(self, request):
        return {"workflow": self.tab_group.kwargs['workflow']}


class WorkflowTemplateTab(tabs.Tab):
    name = _("Template")
    slug = "workflow_template"
    template_name = "nikolaboard/workflowpanel/_workflow_template.html"

    def allowed(self, request):
        #return policy.check(
        #    (("orchestration", "cloudformation:DescribeStacks"),),
        #    request)
        return True

    def get_context_data(self, request):
        return {"workflow_template": self.tab_group.kwargs['workflow_template']}


class WorkflowTabs(tabs.TabGroup):
    slug = "workflowpanel_tabs"
    tabs = (WorkflowTab, WorkflowTemplateTab, )
    sticky = True


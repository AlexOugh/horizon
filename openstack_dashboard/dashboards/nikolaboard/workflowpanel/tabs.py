from django.utils.translation import ugettext_lazy as _
from operator import attrgetter

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


class WorkflowExecutionsTab(tabs.Tab):
    name = _("Executions")
    slug = "workflow_executions"
    template_name = "nikolaboard/workflowpanel/_workflow_executions.html"

    def allowed(self, request):
        #return policy.check(
        #    (("orchestration", "cloudformation:DescribeStacks"),),
        #    request)
        return True

    def get_context_data(self, request):
        workflow = self.tab_group.kwargs['workflow']
        try:
            print '######workflow_name = %s' % workflow.name
            executions = api.nikola.workflow.list_executions(self.request, workflow.name)
            # The stack id is needed to generate the resource URL.
            for execution in executions:
                execution.workflow_id = workflow.id
            executions = sorted(executions, key=attrgetter('created_at'), reverse=True)
        except Exception, ex:
            print ex
            executions = []
        return {"executions": executions,
                "table": tables.ExecutionsTable(request, data=executions), }


class WorkflowTabs(tabs.TabGroup):
    slug = "workflowpanel_tabs"
    tabs = (WorkflowTab, WorkflowTemplateTab, WorkflowExecutionsTab, )
    sticky = True


from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import tabs

from openstack_dashboard import api
from openstack_dashboard.dashboards.nikolaboard.workflowpanel import tables


class WorkflowTab(tabs.TableTab):
    name = _("List")
    slug = "workflow_tab"
    table_classes = (tables.WorkflowTable,)
    template_name = ("horizon/common/_detail_table.html")
    preload = False

    def has_more_data(self, table):
        return self._has_more

    def get_workflow_data(self):
        try:
            marker = self.request.GET.get(
                        tables.WorkflowTable._meta.pagination_param, None)

            workbooks, self._has_more, has_prev_data = api.nikola.workflow.list_workbooks(
                self.request,
                search_opts={'marker': marker, 'paginate': True})

            return workbooks
        except Exception:
            self._has_more = False
            error_message = _('Unable to get instances')
            exceptions.handle(self.request, error_message)
            return []


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


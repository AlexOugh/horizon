
import yaml

from horizon import tabs
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from horizon import exceptions

from openstack_dashboard import api
from openstack_dashboard.dashboards.nikolaboard.workflowpanel import tabs as nikolaboard_tabs


class IndexView(tabs.TabbedTableView):
    # A very simple class-based view...
    tab_group_class = nikolaboard_tabs.WorkflowTabs
    template_name = 'nikolaboard/workflowpanel/index.html'

    #def get_data(self, request, context, *args, **kwargs):
    def get_data(self, request, *args, **kwargs):
        #workbook_id = kwargs['workbook_id']
        workbook_id = None
        try:
            workbook = api.nikola.workflow.get_workbook(
                request,
                workbook_id)
            request.session['workbook_id'] = workbook.id
            request.session['workbook_name'] = workbook.name
            return workbook
        except Exception:
            msg = _("Unable to retrieve workflow.")
            print msg
            exceptions.handle(request, msg, redirect=self.get_redirect_url())


    #@memoized.memoized_method
    def get_template(self, request, **kwargs):
        try:
            #workbook_id = kwargs['workbook_id']
            workbook_id = None
            workflow_template = api.nikola.workflow.get_workbook(
                request,
                workbook_id).definition
            return yaml.safe_dump(workflow_template, indent=2)
        except Exception:
            msg = _("Unable to retrieve workflow template.")
            print msg
            exceptions.handle(request, msg, redirect=self.get_redirect_url())

    def get_tabs(self, request, **kwargs):
        workbook = self.get_data(request, **kwargs)
        workflow_template = self.get_template(request, **kwargs)
        return self.tab_group_class(
            request, workbook=workbook, workflow_template=workflow_template, **kwargs)


    @staticmethod
    def get_redirect_url():
        return reverse('horizon:nikolaboard:workflowpanel:index')

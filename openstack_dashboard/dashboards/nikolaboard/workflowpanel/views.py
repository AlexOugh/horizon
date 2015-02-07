
from horizon import tables
from horizon import tabs
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from horizon import exceptions

from openstack_dashboard import api
from openstack_dashboard.dashboards.nikolaboard.workflowpanel import tables as nikolaboard_tables
from openstack_dashboard.dashboards.nikolaboard.workflowpanel import tabs as nikolaboard_tabs


class IndexView(tables.DataTableView):
    table_class = nikolaboard_tables.WorkflowTable
    template_name = 'nikolaboard/workflowpanel/index.html'

    def __init__(self, *args, **kwargs):
        super(IndexView, self).__init__(*args, **kwargs)
        self._more = None

    def has_prev_data(self, table):
        return self._prev

    def has_more_data(self, table):
        return self._more

    def get_data(self):
        stacks = []
        prev_marker = self.request.GET.get(nikolaboard_tables.WorkflowTable._meta.prev_pagination_param)
        if prev_marker is not None:
            sort_dir = 'asc'
            marker = prev_marker
        else:
            sort_dir = 'desc'
            marker = self.request.GET.get(nikolaboard_tables.WorkflowTable._meta.pagination_param)

        try:
            workbooks, self._more, self._prev = api.nikola.workflow.list_workbooks(
                self.request,
                search_opts={'marker': marker, 'paginate': True})
            if prev_marker is not None:
                workbooks = sorted(workbooks, key=attrgetter('created_at'), reverse=True)
            return workbooks
        except Exception:
            self._prev = False
            self._more = False
            error_message = _('Unable to get instances')
            exceptions.handle(self.request, error_message)
            return []


class DetailView(tabs.TabbedTableView):
    tab_group_class = nikolaboard_tabs.WorkflowTabs
    template_name = 'nikolaboard/workflowpanel/detail.html'

    def get_data(self, request, *args, **kwargs):
        workflow_id = kwargs['workflow_id']
        print kwargs['workflow_id']
        try:
            workbook = api.nikola.workflow.get_workbook(
                request,
                workflow_id)
            request.session['workflow_id'] = workbook.id
            request.session['workflow_name'] = workbook.name
            return workbook
        except Exception:
            msg = _("Unable to retrieve workflow.")
            print msg
            exceptions.handle(request, msg, redirect=self.get_redirect_url())


    #@memoized.memoized_method
    def get_template(self, request, **kwargs):
        try:
            workflow_id = kwargs['workflow_id']
            workflow_template = api.nikola.workflow.get_workbook(
                request,
                workflow_id).definition
            return workflow_template
        except Exception:
            msg = _("Unable to retrieve workflow template.")
            print msg
            exceptions.handle(request, msg, redirect=self.get_redirect_url())


    def get_workflow(self, request, workbook, **kwargs):
        try:
            workflow_id = kwargs['workflow_id']
            workflow = api.nikola.workflow.get_workflow(
                request,
                workbook)
            return workflow
        except Exception:
            msg = _("Unable to retrieve workflow.")
            print msg
            exceptions.handle(request, msg, redirect=self.get_redirect_url())


    def get_tabs(self, request, **kwargs):
        workbook = self.get_data(request, **kwargs)
        #workflow_template = self.get_template(request, **kwargs)
        workflow_template = workbook.definition
        workflow = self.get_workflow(request, workbook, **kwargs)
        return self.tab_group_class(
            request, workbook=workbook, workflow_template=workflow_template, workflow=workflow, **kwargs)


    @staticmethod
    def get_redirect_url():
        return reverse('horizon:nikolaboard:workflowpanel:index')

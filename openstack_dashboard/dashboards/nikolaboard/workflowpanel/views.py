
from horizon import tables
from horizon import tabs
from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from horizon import exceptions
from horizon import forms

from openstack_dashboard import api
from openstack_dashboard.dashboards.nikolaboard.workflowpanel import tables as nikolaboard_tables
from openstack_dashboard.dashboards.nikolaboard.workflowpanel import tabs as nikolaboard_tabs
from openstack_dashboard.dashboards.nikolaboard.workflowpanel import forms as nikolaboard_forms


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
            workflows, self._more, self._prev = api.nikola.workflow.list_workflows(
                self.request,
                search_opts={'marker': marker, 'paginate': True})
            if prev_marker is not None:
                workflows = sorted(workflows, key=attrgetter('created_at'), reverse=True)
            return workflows
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
            workflow = api.nikola.workflow.get_workflow(
                request,
                workflow_id)
            request.session['workflow_id'] = workflow.id
            request.session['workflow_name'] = workflow.name
            return workflow
        except Exception:
            msg = _("Unable to retrieve workflow.")
            print msg
            exceptions.handle(request, msg, redirect=self.get_redirect_url())


    #@memoized.memoized_method
    def get_template(self, request, **kwargs):
        try:
            workflow_id = kwargs['workflow_id']
            workflow_template = api.nikola.workflow.get_workbook(request, workflow_id).definition
            return workflow_template
        except Exception:
            msg = _("Unable to retrieve workflow template.")
            print msg
            exceptions.handle(request, msg, redirect=self.get_redirect_url())


    def get_tabs(self, request, **kwargs):
        workflow = self.get_data(request, **kwargs)
        workflow_template = self.get_template(request, **kwargs)
        return self.tab_group_class(
            request, workflow_template=workflow_template, workflow=workflow, **kwargs)


    @staticmethod
    def get_redirect_url():
        return reverse('horizon:nikolaboard:workflowpanel:index')


class LaunchWorkflowView(forms.ModalFormView):
    template_name = 'nikolaboard/workflowpanel/launch.html'
    modal_header = _("Launch Workflow")
    form_id = "launch_workflow_form"
    form_class = nikolaboard_forms.LaunchWorkflowForm
    submit_label = _("Launch Workflow")
    submit_url = reverse_lazy("horizon:nikolaboard:workflowpanel:launch")
    #success_url = reverse_lazy('horizon:nikolaboard:workflowpanel:detail')

    def get_success_url(self):
        print "get success url : %s" % self.kwargs['workflow_id']
        #url = reverse(self.success_url, args=(self.kwargs['workflow_id'],))
        url = ("/nikolaboard/workflow/%s/" % (self.kwargs['workflow_id']))
        print 'success url = %s' % url
        return url


    def dispatch(self, *args, **kwargs):
        return super(LaunchWorkflowView, self).dispatch(*args, **kwargs)


    def get_form_kwargs(self):
        kwargs = super(LaunchWorkflowView, self).get_form_kwargs()
        return kwargs


    def get_initial(self):
        workflow = self.get_object()
        return {'workflow_id': workflow.id, 'workflow_name':workflow.name, 'workflow_parameters':workflow.parameters}


    def get_context_data(self, **kwargs):
        context = super(LaunchWorkflowView, self).get_context_data(**kwargs)
        workflow = self.get_object()
        context['workflow_id'] = workflow.id
        context['workflow_parameters'] = workflow.parameters
        return context


    def get_object(self):
        workflow_id = self.kwargs['workflow_id']
        try:
            workflow = api.nikola.workflow.get_workflow(
                self.request,
                workflow_id)
        except Exception:
            msg = _("Unable to retrieve workflow.")
            redirect = reverse('horizon:nikolaboard:workflowpanel:index')
            exceptions.handle(self.request, msg, redirect=redirect)
        return workflow


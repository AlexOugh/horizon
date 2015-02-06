from horizon import tabs

from openstack_dashboard.dashboards.nikolaboard.workflowpanel import tabs as nikolaboard_tabs


class IndexView(tabs.TabbedTableView):
    # A very simple class-based view...
    tab_group_class = nikolaboard_tabs.WorkflowTabs
    template_name = 'nikolaboard/workflowpanel/index.html'

    def get_data(self, request, context, *args, **kwargs):
        # Add data to the context here...
        return context

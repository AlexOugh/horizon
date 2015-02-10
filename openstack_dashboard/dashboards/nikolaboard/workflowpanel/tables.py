from django.utils.translation import ugettext_lazy as _

from horizon import tables


class LaunchWorkflowLink(tables.LinkAction):
    name = "create"
    verbose_name = _("Launch Workflow")
    url = "horizon:nikolaboard:workflowpanel:launch"

    def allowed(self, request, user):
        return True


class WorkflowTable(tables.DataTable):
    name = tables.Column("name", verbose_name=_("Name"), link="horizon:nikolaboard:workflowpanel:detail")
    scope = tables.Column("scope", verbose_name=_("Scope"))
    created_at = tables.Column('created_at', verbose_name=_("Created At"))
    updated_at = tables.Column('updated_at', verbose_name=_("Updated At"))

    class Meta:
        name = "workflow"
        verbose_name = _("Workflow")
        row_actions = (LaunchWorkflowLink,)


class ExecutionsTable(tables.DataTable):
    #id = tables.Column('id', verbose_name=_("Id"))
    workflow_name = tables.Column('workflow_name', verbose_name=_("Workflow Name"))
    input = tables.Column("input", verbose_name=_("Input"),)
    output = tables.Column("output", verbose_name=_("Output"),)
    state = tables.Column("state", verbose_name=_("State"),)
    created_at = tables.Column('created_at', verbose_name=_("Created At"))
    #updated_at = tables.Column('updated_at', verbose_name=_("Updated At"))

    class Meta:
        name = "executions"
        verbose_name = _("Workflow Executions")



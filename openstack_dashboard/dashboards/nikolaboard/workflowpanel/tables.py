from django.utils.translation import ugettext_lazy as _

from horizon import tables


class WorkflowTable(tables.DataTable):
    name = tables.Column("name", verbose_name=_("Name"), link="horizon:nikolaboard:workflowpanel:detail")
    scope = tables.Column("scope", verbose_name=_("Scope"))
    created_at = tables.Column('created_at', verbose_name=_("Created At"))
    updated_at = tables.Column('updated_at', verbose_name=_("Updated At"))

    class Meta:
        name = "workflow"
        verbose_name = _("Workflow")
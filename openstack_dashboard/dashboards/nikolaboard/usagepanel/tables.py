from django.utils.translation import ugettext_lazy as _

from horizon import tables


class UsageTable(tables.DataTable):
    meter = tables.Column("meter", verbose_name=_("Meter"))
    #project = tables.Column("project_id", verbose_name=_("Project"))
    resource = tables.Column("resource_name", verbose_name=_("Resource"))
    duration = tables.Column('duration', verbose_name=_("Duration"))
    avg = tables.Column('avg', verbose_name=_("Average"))
    min = tables.Column('min', verbose_name=_("Min"))
    max = tables.Column('max', verbose_name=_("Max"))
    count = tables.Column('count', verbose_name=_("Count"))
    unit = tables.Column('unit', verbose_name=_("Unit"))

    class Meta:
        name = "usage"
        verbose_name = _("Usage")

from django.utils.translation import ugettext_lazy as _

from horizon import tables


class CatalogTable(tables.DataTable):
    name = tables.Column("name", verbose_name=_("Name"), link="horizon:nikolaboard:catalogpanel:detail")
    status = tables.Column("description", verbose_name=_("Description"))
    zone = tables.Column('availability', verbose_name=_("Availability"))

    class Meta:
        name = "catalog"
        verbose_name = _("Service Catalogs")
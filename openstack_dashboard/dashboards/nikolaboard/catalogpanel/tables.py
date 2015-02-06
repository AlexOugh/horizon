from django.utils.translation import ugettext_lazy as _

from horizon import tables


class ServiceCatalogTable(tables.DataTable):
    name = tables.Column("name", verbose_name=_("Name"))
    status = tables.Column("description", verbose_name=_("Description"))
    zone = tables.Column('availability', verbose_name=_("Availability"))
    #image_name = tables.Column('image_name', verbose_name=_("Image Name"))

    class Meta:
        name = "service_catalog"
        verbose_name = _("Service Catalogs")
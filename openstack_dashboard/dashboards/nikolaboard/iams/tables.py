from django.utils.translation import ugettext_lazy as _

from horizon import tables


'''class LaunchCatalogLink(tables.LinkAction):
    name = "create"
    verbose_name = _("Launch Service Catalog")
    url = "horizon:nikolaboard:catalogpanel:launch"

    def allowed(self, request, iam_user):
        return True'''


class IAMTable(tables.DataTable):
    name = tables.Column("name", verbose_name=_("Name"), link="horizon:nikolaboard:iams:detail")
    #status = tables.Column("description", verbose_name=_("Description"))
    #zone = tables.Column('availability', verbose_name=_("Availability"))

    class Meta:
        name = "iam"
        verbose_name = _("IAM")
        #row_actions = (LaunchCatalogLink,)

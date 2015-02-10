from django.utils.translation import ugettext_lazy as _

from horizon import tables


'''class LaunchCatalogLink(tables.LinkAction):
    name = "create"
    verbose_name = _("Launch Service Catalog")
    url = "horizon:nikolaboard:catalogpanel:launch"

    def allowed(self, request, iam_user):
        return True'''


class IAMTable(tables.DataTable):
    sso_uuid = tables.Column('sso_uuid', verbose_name=_("SSO Guid"), link="horizon:nikolaboard:iams:detail")
    op_username = tables.Column('op_username', verbose_name=_("OpenStack User Name"))
    op_user_id = tables.Column('op_user_id', verbose_name=_("OpenStack Id"))
    op_tenant_name = tables.Column('op_tenant_name', verbose_name=_("OpenStack Domain Name"))
    op_keystone_server = tables.Column('op_keystone_server', verbose_name=_("Keystone Server"))
    op_keystone_region = tables.Column('op_keystone_region', verbose_name=_("OpenStack Region"))


    class Meta:
        name = "iam"
        verbose_name = _("IAM")
        #row_actions = (LaunchCatalogLink,)

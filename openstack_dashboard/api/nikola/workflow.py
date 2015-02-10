
import json
from django.conf import settings
from ceilometerclient import client as ceilometer_client


class Workbook():
    
    def __init__(self, workbook_json):
        '''{
            "definition": "---\\nversion: '2.0'\\nname: nikola_poc_sample_alex\\n\\nworkflows:\\n customer_setup:\\n description: Setup a new customer by creating domain/project/admin_user\\n type: direct\\n input:\\n - requester_sso_token\\n - root_op_user_name\\n - root_op_password\\n - root_op_domain_name\\n - email\\n - first_name\\n - last_name\\n - password\\n - company_uuid\\n - auth_url\\n - domain_name\\n - domain_description\\n - project_name\\n - project_description\\n - enabled\\n output:\\n# sso_uuid: $.sso_uuid\\n auth_admin_url: $.auth_admin_url\\n token: $.token\\n domain_id: $.domain_id\\n project_id: $.project_id\\n user_id: $.user_id\\n\\n tasks:\\n create_user_in_sso:\\n action: nikola.serviceAction_sync target='iam' method='create_user_in_sso' requester_sso_token={$.requester_sso_token} email={$.email} first_name={$.first_name} last_name={$.last_name} password={$.password} company_uuid={$.company_uuid} project_name={$.project_name}\\n publish:\\n sso_uuid: $.create_user_in_sso.sso_uuid\\n on-success:\\n - authenticate_in_openstack \\n\\n authenticate_in_openstack:\\n action: nikola.serviceAction_sync target='openstack' method='authenticate' auth_url={$.auth_url} user_name={$.root_op_user_name} password={$.root_op_password} domain_name={$.root_op_domain_name}\\n publish:\\n auth_admin_url: $.authenticate_in_openstack.auth_admin_url\\n token: $.authenticate_in_openstack.token\\n on-success:\\n - create_domain_in_openstack\\n\\n create_domain_in_openstack:\\n action: nikola.serviceAction_sync target='openstack' method='create_domain' domain_name={$.domain_name} description={$.domain_description} enabled={$.enabled} auth_admin_url={$.auth_admin_url} admin_token={$.token}\\n publish:\\n domain_id: $.create_domain_in_openstack.id\\n on-success:\\n - create_project_in_openstack\\n\\n create_project_in_openstack:\\n action: nikola.serviceAction_sync target='openstack' method='create_project' project_name={$.project_name} description={$.project_description} enabled={$.enabled} domain_id={$.domain_id} auth_admin_url={$.auth_admin_url} admin_token={$.token}\\n publish:\\n project_id: $.create_project_in_openstack.id\\n on-success:\\n - create_user_in_openstack\\n\\n create_user_in_openstack:\\n action: nikola.serviceAction_sync target='openstack' method='create_user' user_name={$.email} email={$.email} password={$.password} enabled={$.enabled} domain_id={$.domain_id} auth_admin_url={$.auth_admin_url} admin_token={$.token}\\n publish:\\n user_id: $.create_user_in_openstack.id\\n on-success:\\n - add_admin_role_to_user_in_openstack\\n\\n add_admin_role_to_user_in_openstack:\\n action: nikola.serviceAction_sync target='openstack' method='add_admin_role_to_user' user_id={$.user_id} domain_id={$.domain_id} auth_admin_url={$.auth_admin_url} admin_token={$.token}\\n on-success:\\n - associate_project_to_user_in_openstack\\n\\n associate_project_to_user_in_openstack:\\n action: nikola.serviceAction_sync target='openstack' method='associate_project_to_user' project_id={$.project_id} user_id={$.user_id} auth_admin_url={$.auth_admin_url} admin_token={$.token}\\n on-success:\\n - store_user_info_to_iam\\n\\n store_user_info_to_iam:\\n action: nikola.serviceAction_sync target='iam' method='store_user_info' sso_uuid={$.sso_uuid} email={$.email} first_name={$.first_name} last_name={$.last_name} password={$.password} company_uuid={$.company_uuid} project_name={$.project_name}\\n publish:\\n sso_uuid: $.store_user_info_to_iam.sso_uuid\\n",
            "name": "nikola_poc_sample_alex",
            "tags": [ ],
            "created_at": "2015-02-06 15:55:16",
            "updated_at": null,
            "scope": "private",
            "id": "4d25f69b-3ead-4bac-954e-c13aa392c06f"
        }'''
        self.id = workbook_json['id']
        self.name = workbook_json['name']
        self.tags = workbook_json['tags']
        self.created_at = workbook_json['created_at']
        self.updated_at = workbook_json['updated_at']
        self.scope = workbook_json['scope']
        self.definition = workbook_json['definition']


class Workflow():
    
    def __init__(self, workflow_json):
        '''{
            "definition": null,
            "scope": "private",
            "name": "nikola_poc_sample.customer_setup",
            "tags": null,
            "input": "requester_sso_token, root_op_user_name, root_op_password, root_op_domain_name, email, first_name, last_name, password, company_uuid, auth_url, domain_name, domain_description, project_name, project_description, enabled",
            "created_at": "2015-02-06 06:16:44",
            "updated_at": "2015-02-06 09:57:02",
            "id": "29bbe30c-8935-43fc-8e5c-a9861e1f08d5"
        }'''
        self.id = workflow_json['id']
        self.name = workflow_json['name']
        self.input = workflow_json['input']
        self.tags = workflow_json['tags']
        self.created_at = workflow_json['created_at']
        self.updated_at = workflow_json['updated_at']
        self.scope = workflow_json['scope']
        self.definition = workflow_json['definition']
        self.parameters = self.input.split(',')


class Execution():
    
    def __init__(self, execution_json):
        '''{
            "state_info": null,
            "workflow_name": "nikola_poc_test.customer_setup",
            "created_at": "2015-02-09 22:14:45",
            "updated_at": "2015-02-09 22:14:47",
            "state": "SUCCESS",
            "output": "{'project_id': 'f42a53114a934a179013d5a06034c622', 'token': 'd20a618008924799b5b19c35850a830a', 'auth_admin_url': 'http://r1-controller:35357/v2.0', 'domain_id': 'eaf9611bc60e4f2ebaea1468b504cdaf', 'user_id': '5fc61f0601ee4cd2a0ca5e4b8ccd2cad'}",
            "input": "{'domain_name': 'poc_domain_1', 'email': 'poc_user_1@a.com', 'requester_sso_token': '3018138b45d23850ebe49c0c97faa5a60f06a0e8407b7557bc72fca9764ff523', 'root_op_password': 'password', 'enabled': 'True', 'root_op_user_name': 'admin', 'company_uuid': '76c6f530-40c1-446d-a5d5-a66e78605149', 'auth_url': 'http://172.20.1.50:5000/v3/', 'password': 'Sungard05', 'project_name': 'poc_project_1', 'domain_description': 'Domain created for poc', 'first_name': 'poc_first_1', 'project_description': 'Project created for poc', 'last_name': 'poc_last_1', 'root_op_domain_name': 'default'}",
            "id": "f85fd723-62b2-4e10-a896-c9b00a9edaf8"
        }'''
        self.id = execution_json['id']
        self.workflow_name = execution_json['workflow_name']
        self.created_at = execution_json['created_at']
        self.updated_at = execution_json['updated_at']
        self.state = execution_json['state']
        self.output = execution_json['output']
        self.input = execution_json['input']
        self.state_info = execution_json['state_info']


def list_workbooks(request, search_opts=None):
    
    from nikola_api import NikolaAPI
    nikapi = NikolaAPI()
    res = nikapi.send(url='/useast1/nikola/r2/workflow/list_workbooks', data='{"all":null}')
    workbooks = []
    for workbook in res['result']['result']['workbooks']:
        workbooks.append(Workbook(workbook))

    has_prev_data = False
    has_more_data = False
    return (workbooks, has_more_data, has_prev_data)


def list_workflows(request, search_opts=None):
    
    from nikola_api import NikolaAPI
    nikapi = NikolaAPI()
    res = nikapi.send(url='/useast1/nikola/r2/workflow/list_workflows', data='{"all":null}')
    workflows = []
    for workflow in res['result']['result']['workflows']:
        workflows.append(Workflow(workflow))

    has_prev_data = False
    has_more_data = False
    return (workflows, has_more_data, has_prev_data)


def get_workbook(request, workflow_id):

    workflow = get_workflow(request, workflow_id)
    if workflow is None:    return None
    (workbooks, has_more_data, has_prev_data) = list_workbooks(request)
    for workbook in workbooks:
        if workbook.name == workflow.name.split('.')[0]:  return workbook
    return None


def get_workflow(request, workflow_id):
    
    (workflows, has_more_data, has_prev_data) = list_workflows(request)
    for workflow in workflows:
        if workflow.id == workflow_id:    return workflow
    return None


def launch_workflow(request, workflow_name, params):
    
    #auth_ref = request.session['auth_ref']
    #workflow = auth_ref.get('workflow')
    #endpoint = next(ep['url'] for ep in next(s['endpoints'] for s in workflow if s['name'] == 'heat') if ep['interface']=='public')
    #token = auth_ref['auth_token']  
    
    from nikola_api import NikolaAPI
    nikapi = NikolaAPI()
    print workflow_name, params
    data = json.dumps({"workflow_definition":workflow_name, "input_json":params})
    print data
    res = nikapi.send(url='/useast1/nikola/r2/workflow/start', data=data)
    print res
    return res['result']['result']['id']


def list_executions(request, workflow_name):

    from nikola_api import NikolaAPI
    nikapi = NikolaAPI()
    res = nikapi.send(url='/useast1/nikola/r2/workflow/list_executions', data=json.dumps({"workflow_definition":workflow_name}))
    print "####", res
    executions = []
    for execution in res['result']['result']:
        executions.append(Execution(execution))

    return executions




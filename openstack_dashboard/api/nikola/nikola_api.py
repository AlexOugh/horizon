
#import logging
import httplib, urllib
import simplejson as json

class NikolaAPI():
    
    def _get_headers(self):
        #if self.cookie is None:    raise Exception, "no cookie available"
        headers = {'content-type':'text/plain'}
        #headers['cookie'] = self.cookie
        return headers


    def _request_get(self, server, url, params):
        try:
            conn = httplib.HTTPConnection(server)
            headers = self._get_headers()
            task_url = '%s?%s' % (url, urllib.urlencode(params))
            conn.request("GET", task_url, headers=headers)
            response = conn.getresponse()
            content = response.read()
            #print "######"
            #print content
            '''res_json = json.loads(content).values()[0]
            if 'errorcode' in res_json:
                raise Exception, res_json['errortext']
            if ret_attr_name:
                if ret_attr_name in res_json:
                    return res_json[ret_attr_name]
                else:
                    return []'''
            res_json = json.loads(content)
            return res_json
        except Exception, ex:
            print ex
            raise ex


    def _request_post(self, server, url, param_json):
        try:
            conn = httplib.HTTPConnection(server)
            headers = self._get_headers()
            if param_json:
                if headers:
                    conn.request("POST", url, json.dumps(param_json), headers=headers)
                else:
                    conn.request("POST", url, json.dumps(param_json))
            else:
                if headers:
                    conn.request("POST", url, headers=headers)
                else:
                    conn.request("POST", url)
            response = conn.getresponse()
            content = response.read()
            #print "######"
            #print content
            res_json = json.loads(content)
            return res_json
        except Exception, ex:
            print ex
            raise ex


    def send(self, host='172.20.1.14:3000', url='/useast1/nikola/r2/', method='POST', data=None):
        
        request_type = method
        if data:
            params = json.loads(data)
            #print params
        else:
            params = None
        
        if params:
            for key in params.keys():
                type_name = type(params[key]).__name__
                if type_name == 'dict' or type_name == 'list':
                    params[key] = json.dumps(params[key])
                elif type_name != 'str':
                    params[key] = str(params[key])
        
            #params = json.dumps(params)
            #print params

        if request_type == 'POST':
            ret = self._request_post(host, url, params)
        else:
            ret = self._request_get(host, url, params)
        #ret = self._request(host, url, request_type, data)
        #print ret
        return {'result':ret}



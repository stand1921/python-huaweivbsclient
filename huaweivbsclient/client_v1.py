import exceptions
import requests


class Client(object):
    """Client for the API.
    :param string session: Keystoneauth session.
    :param string token: Token used for HuaWei VBS access.
    :param string endpoint: HuaWei VBS endpoint url.
    :param string tenant_id: The project ID used for context.
    """

    def __init__(self, token=None, tenant_id=None, endpoint=None, **kwargs):
        """Initialize a new client for the API."""
        self.token = token
        self.tenant_id = tenant_id
        self.endpoint = endpoint
        self.headers = {
            'Content-Type': 'application/json;charset=utf8',
            'X-Auth-Token': token,
        }

    def _request(self, method, url, **kwargs):
        """Base request."""
        res = requests.request(method, url, headers=self.headers,
                               verify=False, **kwargs)
        if res.status_code != 200:
            print res.text
            res.raise_for_status()
        result = res.json()
        if 'error' in result:
            raise exceptions.ServiceError(
                result['error']['code'], result['error']['message'])
        return result

    def _get(self, url, **kwargs):
        return self._request('GET', url, **kwargs)

    def _post(self, url, **kwargs):
        return self._request('POST', url, **kwargs)

    def backup_list(self):
        """Backup list api."""
        url = self.endpoint + '/v2/%s/backups' % self.tenant_id
        return self._get(url)

    def backup_create(self, volume_id, name, description=None):
        """Backup create api."""
        data = {
            'backup': {
                'volume_id': volume_id,
                'name': name,
            }
        }
        if description:
            data['backup']['description'] = description
        url = self.endpoint + '/v2/%s/cloudbackups' % self.tenant_id
        return self._post(url, json=data)

    def backup_delete(self, backup_id):
        """Backup delete api."""
        url = self.endpoint + '/v2/%s/cloudbackups/%s' % \
                              (self.tenant_id, backup_id)
        return self._post(url)

    def backup_restore(self, backup_id, volume_id):
        """Backup restore api."""
        url = self.endpoint + '/v2/%s/cloudbackups/%s/restore' % \
                              (self.tenant_id, backup_id)
        data = {
            'restore': {
                'volume_id': volume_id
            }
        }
        return self._post(url, json=data)

    def backup_query_status(self, job_id):
        """Backup query job status api."""
        url = self.endpoint + '/v1/%s/jobs/%s' % \
                              (self.tenant_id, job_id)
        return self._get(url)

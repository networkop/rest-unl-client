import requests


class RestServer(object):

    def __init__(self, address):
        self.cookies = None
        self.base_url = '/'.join(['http:/', address, 'api'])
        self.user, self.pwd = '', ''

    def set_credentials(self, user, pwd):
        self.user, self.pwd = user, pwd
        return None

    def _send_request(self, method, path, data=None):
        response = None
        url = self.base_url + path
        try:
            response = requests.request(method, url,  json=data, cookies=self.cookies)
        except requests.exceptions.RequestException as e:
            print('*** Error calling %s: %s', url, e.message)
        if self.cookies and 400 < response.status_code < 499:
            self.login(self.user, self.pwd)
            response = requests.request(method, url,  json=data, cookies=self.cookies)
        return response

    def get_object(self, api_call, data=None):
        return self._send_request('GET', api_call, data)

    def add_object(self, api_call, data=None):
        return self._send_request('POST', api_call, data)

    def update_object(self, api_call, data=None):
        return self._send_request('PUT', api_call, data)

    def del_object(self, api_call, data=None):
        return self._send_request('DELETE', api_call, data)

    def set_cookies(self, cookie):
        self.cookies = cookie
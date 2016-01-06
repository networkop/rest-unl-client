import requests


class RestServer(object):

    def __init__(self, address):
        self.cookies = None
        self.base_url = '/'.join(['http:/', address, 'api'])

    def _send_request(self, method, path, data=None):
        response = None
        url = self.base_url + path
        try:
            response = requests.request(method, url,  json=data, cookies=self.cookies)
        except requests.exceptions.RequestException as e:
            print('*** Error calling %s: %s', url, e.message)
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
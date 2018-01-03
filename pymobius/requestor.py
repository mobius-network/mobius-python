import requests


class ApiError(Exception):
    """Base exception class for exceptions while communicating with the API."""


class Requestor:

    def __init__(self, api_key=None, host=None, version=None, auth=None):
        self.api_key = api_key
        self.host = host if host is not None else 'https://mobius.network/api'
        self.version = version if version is not None else 'v1'
        self.auth = auth

    def headers(self):
        result = dict()

        if self.auth:
            result['Authorization'] = self.auth

        result['x-api-key'] = self.api_key

        return result

    def url(self, resource, action):
        return '{}/{}/{}/{}'.format(self.host, self.version, resource, action)

    def request(self, method, resource, action, **payload):
        url = self.url(resource, action)
        headers = self.headers()

        request = requests.get if method == 'GET' else requests.post
        data = dict(params=payload) if method == 'GET' else dict(data=payload)

        response = request(url, headers=headers, **data)

        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            err_json = response.json()
            raise ApiError(err_json.get('error').get('message'))
        else:
            return response.json()

    def get(self, resource, action, **payload):
        return self.request('GET', resource, action, **payload)

    def post(self, resource, action, **payload):
        return self.request('POST', resource, action, **payload)

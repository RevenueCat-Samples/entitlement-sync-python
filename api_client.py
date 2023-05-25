"""

"""
from urllib.parse import quote

import requests

API_VERSION_URLS = {
    1: 'https://api.revenuecat.com/v1',
    2: 'https://api.revenuecat.com/v2',
}


def api_url_for_version(api_version: int) -> str:
    try:
        return API_VERSION_URLS[api_version]
    except KeyError:
        raise ValueError('Unknown API version. Valid versions are `1` or `2`')


class RevenueCatClient:
    """Client to make HTTP requests to RevenueCat's V2 API.

    As of May, 2023, the Customers endpoints are in closed-beta, so we still fallback to the V1
    subscribers endpoint for now.
    """

    def __init__(self, secret_api_key: str, project_id: str, api_version=2):
        self.api_key = secret_api_key
        self.project_id = quote(project_id)
        self.api_version = api_version
        self.api_url = api_url_for_version(api_version)

    def _make_request(self, method, url, data=None, json=None, params=None, headers=None,
                      api_version: int = None,
                      **kwargs) -> requests.Response:
        # TODO: logging, error handling, metrics, rate limiting, retries
        # TODO: headers
        # TODO: timeouts
        # TODO: pagination
        # TODO: proxies
        # TODO: expandables
        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {self.api_key}'
        }
        api_url = self.api_url if api_version is None else api_url_for_version(api_version)
        full_url = f'{api_url}{url}'
        return requests.request(method, full_url, data=data, params=params, json=json, headers=headers,
                                **kwargs)

    def post(self, url, data=None, json=None, params=None, api_version=None) -> requests.Response:
        """Sends a POST request.

        :param url: URL for the new :class:`Request` object.
        :param data: (optional) Dictionary, list of tuples, bytes, or file-like
            object to send in the body of the :class:`Request`.
        :param json: (optional) A JSON serializable Python object to send in the body of the
        :class:`Request`.
        :param **kwargs: Optional arguments that ``request`` takes.
        :return: :class:`Response <Response>` object
        :rtype: requests.Response
        """
        return self._make_request('POST', headers={'Content-Type': 'application/json'})

    def get(self, url, params=None, api_version=None, **kwargs) -> requests.Response:
        """
        :param api_version:
        :param url: URL for the new :class:`Request` object.
        :param params: (optional) Dictionary, list of tuples or bytes to send
            in the query string for the :class:`Request`.
        :param kwargs: Optional arguments that ``request`` takes.
        """
        response = self._make_request('GET', url, params=params, api_version=api_version, **kwargs)
        return response.json()

    def handle_error(self):
        """
        Code	Name	        Description
        200 	OK	            Processes as expected
        201 	Created	        Entity was created
        202 	Accepted    	Request acknowledged, but cannot be processed in real time (for
        instance, async job)
        204 	No content
        400 	Bad Request  	Client error
        401 	Unauthorized	Not authenticated
        403 	Forbidden   	Authorization failed
        404 	Not Found   	No resource was found
        409 	Conflict    	Uniqueness constraint violation
        418 	I'm a teapot	RevenueCat refuses to brew coffee
        422 	Unprocessable entity	The request was valid and the syntax correct, but we were
        unable to process the contained instructions.
        423 	Locked      	The request conflicted with another ongoing request
        429 	Too Many Requests	Being rate limited
        500 	Internal Server Error
        502 	Bad Gateway	Invalid response from an upstream server
        503 	Service Unavailable	There wasn’t a server to handle the request
        504 	Gateway Timeout	We could not get the response in time from the upstream server
        """

    def get_projects(self):
        return self.get('/projects')

    def get_apps(self):
        response = self.get(f'/projects/{self.project_id}/apps')
        return response.json()

    def get_app(self, app_id: str):
        return self.get(f'/projects/{self.project_id}/apps/{quote(app_id)}')

    def get_products(self):
        return self.get(f'/projects/{self.project_id}/products')

    def get_product(self, product_id: str):
        return self.get(f'/projects/{self.project_id}/products/{quote(product_id)}')

    def get_entitlement(self, entitlement_id: str):
        return self.get(f'/projects/{self.project_id}/entitlements/{quote(entitlement_id)}')

    def get_entitlements(self):
        return self.get(f'/projects/{self.project_id}/entitlements')

    def get_entitlement_products(self, entitlement_id: str):
        return self.get(
            f'/projects/{self.project_id}/entitlements/'
            f'{quote(entitlement_id)}/products')

    def get_offering(self, offering_id: str):
        return self.get(f'/projects/{self.project_id}/offerings/{quote(offering_id)}')

    def get_offerings(self, offering_id: str):
        return self.get(f'/projects/{self.project_id}/offerings')

    def get_packages(self, offering_id: str):
        return self.get(
            f'/projects/{self.project_id}/offerings/{quote(offering_id)}/packages')

    def get_package(self, package_id: str):
        return self.get(f'/projects/{self.project_id}/packages/{quote(package_id)}')

    def get_package_products(self, package_id):
        return self.get(f'/projects/{self.project_id}/packages/{quote(package_id)}/products')

    def get_subscriber(self, subscriber_id: str):
        """
        :param subscriber_id: App user ID
        :return: https://www.revenuecat.com/reference/subscribers
        """
        return self.get(f'/subscribers/{quote(subscriber_id)}',
                        api_version=1)

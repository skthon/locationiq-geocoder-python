"""
Python API client wrapper for the LocationIQ Geocoding service

LocationIQ provides 10,000 requests/day for free. You can signup here to get the API Key : https://locationiq.org/
API documentation is available on https://locationiq.org/docs
"""

import requests
import json
from requests.exceptions import RequestException


class LocationIq(object):
    """LocationIQ API client wrapper."""

    def __init__(self, key=None, format="json", addressdetails=1, limit=10, params={}, timeout=None, test_mode=False):
        """Initialize the API Client wrapper

        :param key: LocationIQ API key. You can signup here to get the api key: https://locationiq.org
        :param format: Output response format. json, xml are available formats. (Defaults to json)
        :param addressdetails: Include a breakdown of the address into elements. Accepted values are 0 or 1.
        :param limit: Limit the number of returned results. Default is 10. Max is 50.
        :param params: Set extra params to return desired results. This includes viewbox, zoom, postalcode etc.
        :param timeout: Connect and read timeout in seconds.  Specify a tuple (connect, read) to specify each timeout individually.
        :param test_mode: Set to True to enable test mode. Defaults to False.
        """

        self.key = key
        self.timeout = timeout
        self.test_mode = test_mode
        self.params = {
            "format": format,
            "addressdetails": addressdetails,
            "limit": limit,
            "accept-language": "en"
        }

        # Content headers
        self.headers = {'content-type': 'application/json'}

        extra_params = {
            "viewbox": [],
            "bounded": 0,
            "zoom": 18,
            "street": None,
            "city": None,
            "county": None,
            "state": None,
            "country": None,
            "postalcode": None
        }

        # If user includes any extra params, the update the self.params object
        for param, value in params:
            if param in extra_params:
                self.params.update({param: value})

    def geocode(self, query=None):
        """Search the given string or address from LocationIQ Geocoder
        :param query: String to search for
        :returns result: A list of addresses matching the given search string
        """

        url = "https://locationiq.org/v1/search.php"
        data = {
            "key": self.key,
            "q": query
        }
        data.update(self.params)

        r = LocationIqRequest(url)
        r.get(data, self.headers)
        return r.response

    def reverse_geocode(self, lat, lon):
        """Get the address for the given latitude, longitude from  LocationIQ reverse geocoder.
        :param lat: Latitude
        :param lon: Longitude
        :returns result: dict
        """

        url = "https://locationiq.org/v1/reverse.php"

        data = {
            "key": self.key,
            "lat": lat,
            "lon": lon
        }
        data.update(self.params)

        r = LocationIqRequest(url)
        r.get(data, self.headers)
        return r.response


class LocationIqRequest(object):
    """
    Helper class for making requests.
    :param url: Base url or endpoint url to send the requests
    """

    def __init__(self, url=None):
        """Initialize request object."""
        self.url = url
        self.data = None
        self.code = None
        self.response = None

    def request(self, method='GET', params={}, headers={}):
        """
        Make a request.
        If the request was successful (i.e no exceptions), you can find the
        HTTP response code in self.code and the response body in self.value.
        :param method: Request method (Only GET supported)
        :param params: Request parameters
        :param headers: Request headers
        """
        self.data = None
        self.code = None

        kwargs = dict(
            params=params,
            headers=headers,
        )

        request_func = getattr(requests, method.lower())

        try:
            res = request_func(self.url, **kwargs)
            self.data = res.json()
            self.code = res.status_code
            res.raise_for_status()
            return self.data
        except requests.exceptions.RequestException as err:
            # Concatenate the error code and the error message
            return LocationIqError.factory(self.code, self.data['error'])
        except requests.exceptions.HTTPError as errh:
            return "Http Error:", errh
        except requests.exceptions.ConnectionError as errc:
            return "Error Connecting:", errc
        except requests.exceptions.Timeout as errt:
            return "Timeout Error:", errt

    def get(self, params: object = {}, headers: object = {}):
        """
        Make a GET request
        :param params: Request parameters to send in the url
        :param headers: Request Headers
        :return response: Response
        """
        self.response = self.request("GET", params=params, headers=headers)


class LocationIqError(Exception):
    """Exception raised when the server returns a known HTTP error code.

    Known HTTP error codes include:
    * 404 Unable to geocode
    * 401 Invalid key or key not active
    * 400 Invalid request
    * 429 Request Ratelimited error
    * 500 Error on server's side
    """

    @staticmethod
    def factory(err_code, err_message):
        """Create exceptions through a Factory based on the HTTP error code."""
        if err_code == 404:
            # No location or places were found for the given input
            return LocationIqErrorMessage.display(err_code, "No location or places were found for the given input")
        elif err_code == 401:
            # An invalid API key was provided
            return LocationIqErrorMessage.display(err_code, "An invalid API key was provided")
        elif err_code == 400:
            # Required parameters are missing, or invalid.
            return LocationIqErrorMessage.display(err_code, "Required parameters are missing, or invalid.")
        elif err_code == 429:
            # Request exceeded the per-second / minute / day rate-limits set on your account
            return LocationIqErrorMessage.display(err_code, "Request exceeded the per-second / minute / day rate-limits set on your account")
        else:
            return LocationIqErrorMessage.display(err_code, err_message)


class LocationIqErrorMessage(LocationIqError):
    """
    Prepare the error string to be returned to the user
    :param error_code: Response code
    :param err_message: Error message to be displayed
    """

    @staticmethod
    def display(err_code, err_message):
        return "Response Code %s: %s" % (err_code, err_message)

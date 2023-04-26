import requests
from enum import Enum
from typing import Optional, Any, Dict


class ErrorCodes(Enum):
    """

    ErrorCodes

    Sentino API error codes

    Args:
        Enum (int): An enumeration of error codes.
    """

    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    NOT_FOUND = 404
    METHOD_NOT_ALLOWED = 405
    NOT_ACCEPTABLE = 406
    TOO_MANY_REQUESTS = 429
    INTERNAL_SERVER_ERROR = 500
    SERVICE_UNAVAILABLE = 503


class SentinoAPIWrapper:
    """

    A wrapper for the Sentino API,

    Attributes:
        BASE_URL (str): The base URL for the Sentino API.
        ERROR_CODES (Dict[int, str]): A dictionary of error codes and their corresponding messages.

    Methods:
        score_text
        get_inventory
        classify
    """

    BASE_URL: str = "https://api.sentino.org"
    ERROR_CODES: Dict[int, str] = {
        ErrorCodes.BAD_REQUEST.value: "Bad Request -- Your request is invalid.",
        ErrorCodes.UNAUTHORIZED.value: "Unauthorized -- Your Sentino API token is wrong.",
        ErrorCodes.NOT_FOUND.value: "Not Found -- The endpoint is not found.",
        ErrorCodes.METHOD_NOT_ALLOWED.value: "Method Not Allowed -- You tried to access an invalid method.",
        ErrorCodes.NOT_ACCEPTABLE.value: "Not Acceptable -- You requested a format that isn't json.",
        ErrorCodes.TOO_MANY_REQUESTS.value: "Too Many Requests -- You're requesting too many things! Slow down!",
        ErrorCodes.INTERNAL_SERVER_ERROR.value: "Internal Server Error -- We had a problem with our server. Try again later.",
        ErrorCodes.SERVICE_UNAVAILABLE.value: "Service Unavailable -- We're temporarily offline for maintenance. Please try again later."
    }

    def __init__(self, api_key: str) -> None:
        """
        Initialize a new instance of the class.

        Args:
            api_key (str): The API key to use for authentication.

        Returns:
            None
        """
        self.api_key = api_key
        self.baseurl = self.BASE_URL
        self.headers = {
            "Authorization": f"Token {self.api_key}",
            "Content-Type": "application/json"
        }

    def _make_request(self, url: str, method: str, data: Optional[Dict] = None) -> Any:
        """
        Makes an HTTP request to the given URL using the specified HTTP method and data.

        Args:
            url (str): The URL to send the request to.
            method (str, optional): The HTTP method to use. Must be one of 'GET', 'POST', 'PUT', or 'DELETE'. Defaults to 'get'.
            data (dict, optional): The data to send with the request, as a dictionary. Defaults to None.

        Raises:
            ValueError: If an invalid HTTP method is specified.

        Returns:
            The response from the server, as returned by the _handle_response method.
        """
        if method == "get":
            response = requests.get(url, headers=self.headers)
        elif method == "post":
            response = requests.post(url, headers=self.headers, json=data)
        return self._handle_response(response)

    def _handle_response(self, response: requests.Response) -> Any:
        """Process a response from the API and return its JSON content.

        Args:
            response: The response object returned by the API request.

        Raises:
            Exception: If the response status code is in the ERROR_CODES dictionary.

        Returns:
            The JSON content of the response.

        """
        if response.status_code in self.ERROR_CODES:
            error_message = self.ERROR_CODES[response.status_code]
            raise Exception(f"Request failed with status code {response.status_code}: {error_message}")
        return response

    def score_text(self, text: str, lang: str = "en") -> Dict[str, Any]:
        """
        Score Text: https://bot.sentino.org/api#score-text

        Extract psychologically meaningful information from a self-description of a person in natural language.

        The text is split into sentences and each sentence is labeled with corresponding topic and inventory.

        Args:
            text: A string containing the text to analyze.
            lang: An optional string representing the language of the text. Defaults to "en".

        Returns:
            A dictionary containing the scores for the Big Five personality traits and their facets.
            The keys are "openness", "conscientiousness", "extraversion", "agreeableness", and "neuroticism".
            The values are dictionaries with the scores for the facets of each trait.
            Each facet is a string representing a specific aspect of the trait, and its value is a float between 0 and 1.

        """
        url = f"{self.BASE_URL}/score"
        payload = {
            "text": text,
            "inventories": ["big5"],
            "lang": lang
        }
        response = self._make_request(url, method='post', data=payload)
        return self._handle_response(response)

    def get_inventories(self):
        """
        Get Inventories: https://bot.sentino.org/api#inventories
        This endpoint shows all available personality inventories.

        Returns:
            A list of inventories returned by the API.
        """
        url = f"{self.BASE_URL}/inventories"
        response = self._make_request(url, method='get')
        return self._handle_response(response)

    def classify(self, text: str) -> dict:
        """
        Classify Text: https://bot.sentino.org/api#item-analysis
        The result is a probability of belonging to a certain category with a range of [0, +1]). Probability higher than 0.5 is considered relevant.

        Args:
            text (str): The text to classify.

        Returns:
            dict: A dictionary containing the classification results.

        Raises:
            SentinoAPIError: If the API request fails or the response is invalid.
        """
        url = f"{self.BASE_URL}/item/classify"
        payload = {
            "text": text
        }
        response = self._make_request(url, method='post', data=payload)
        return self._handle_response(response)

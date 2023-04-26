import unittest
import os
from sentinoapi import SentinoAPIWrapper


class SentinoAPIWrapperTest(unittest.TestCase):
    def setUp(self):
        self.api_key = os.environ.get("SENTINO_API_KEY")

    def test_score_text(self):
        sapi = SentinoAPIWrapper(self.api_key)
        # Test with valid text
        text = "I am a happy person."
        scores = sapi.score_text(text)
        self.assertIsNotNone(scores)

    def test_get_inventories(self):
        sapi = SentinoAPIWrapper(self.api_key)
        inventories = sapi.get_inventories()
        self.assertIsNotNone(inventories)

    def test_classify(self):
        sapi = SentinoAPIWrapper(self.api_key)
        # Test with valid text
        text = "I am brave."
        classification = sapi.classify(text)
        print(classification)
        self.assertIsNotNone(classification)

    def test_make_request(self):
        # Create a new instance of the `SentinoAPIWrapper` class.
        sapi = SentinoAPIWrapper(self.api_key)
        # Make a request to the Sentino API to get the list of inventories.
        response = sapi._make_request("https://api.sentino.org/inventories", method="get")
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), dict)
        self.assertIn("big5", response.json()['inventories'])

if __name__ == "__main__":
    unittest.main()

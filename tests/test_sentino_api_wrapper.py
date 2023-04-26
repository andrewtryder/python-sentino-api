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


if __name__ == "__main__":
    unittest.main()

import unittest
from llm_client import LLMClient


class FakeProvider:

    def generate(self, prompt):
        return "Test response"


class TestLLMClient(unittest.TestCase):

    def test_generate(self):
        client = LLMClient(FakeProvider())
        result = client.generate("Hello")

        self.assertEqual(result, "Test response")


if __name__ == "__main__":
    unittest.main()
import unittest
import random
from questions import *

class TestQuestions(unittest.TestCase):

    data = {}

    def setUp(self):
        directory = './corpus/'
        self.data = load_files(directory)

    def test_load_files(self):
        # test keys of data dictiorary
        self.assertEqual(set(self.data.keys()), {'artificial_intelligence.txt','machine_learning.txt', 'natural_language_processing.txt','neural_network.txt', 'probability.txt','python.txt'})
        # test strings in dictionary
        self.assertIsInstance(self.data['natural_language_processing.txt'], str)
        self.assertGreater(len(self.data['natural_language_processing.txt']), 0)

    def test_tokenize(self):
        tokens = tokenize(self.data['natural_language_processing.txt'])
        samples = random.sample(tokens, 5)
        for sample in samples:
            print(sample)
            self.assertTrue(sample.islower())
    
if __name__ == '__main__':
    unittest.main()

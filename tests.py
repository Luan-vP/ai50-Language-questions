import unittest
from questions import *

class TestQuestions(unittest.TestCase):

    def setUp(self):
        pass

    def test_load_files(self):
        directory = './corpus/'
        data = load_files(directory)
        # test keys of data dictiorary
        self.assertEqual(set(data.keys()), {'artificial_intelligence.txt','machine_learning.txt', 'natural_language_processing.txt','neural_network.txt', 'probability.txt','python.txt'})
        # test strings in dictionary
        self.assertIsInstance(data['natural_language_processing.txt'], str)
        self.assertGreater(len(data['natural_language_processing.txt']), 0)
    
if __name__ == '__main__':
    unittest.main()

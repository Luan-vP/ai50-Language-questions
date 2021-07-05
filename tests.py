import unittest
import random
from questions import *

# test string: unanswered mind discovered solve creating time

class TestQuestions(unittest.TestCase):

    data = {}

    def setUp(self):
        directory = './corpus/'
        self.data = load_files(directory)
        self.documents = {}
        for filename, text in self.data.items():
            self.documents[filename] = tokenize(text)


    def test_load_files(self):
        # test keys of data dictiorary
        self.assertEqual(set(self.data.keys()), {'artificial_intelligence.txt','machine_learning.txt', 'natural_language_processing.txt','neural_network.txt', 'probability.txt','python.txt'})
        # test strings in dictionary
        self.assertIsInstance(self.data['natural_language_processing.txt'], str)
        self.assertGreater(len(self.data['natural_language_processing.txt']), 0)

    def test_tokenize(self):
        tokens = tokenize(' '.join(list(self.data.values())))
        samples = random.sample(tokens, 1000)
        for stopword in nltk.corpus.stopwords.words("english"):
            self.assertNotIn(stopword, tokens)
        for punct in string.punctuation:
            self.assertNotIn(punct, tokens)

    def test_compute_idfs(self):
        idfs = compute_idfs(self.documents)
        tests = {'unanswered': 1.791759469228055, 'mind': 1.0986122886681098, 'discovered': 0.6931471805599453, 'solve': 0.4054651081081644, 'creating': 0.1823215567939546, 'time': 0.0}
        for prompt, answer in tests.items():
            self.assertAlmostEqual(idfs[prompt], answer)

    
if __name__ == '__main__':
    unittest.main()

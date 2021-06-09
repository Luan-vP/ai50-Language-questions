import nltk
nltk.download('punkt')
nltk.download('stopwords')
import string
import math
import sys
import os
from collections import Counter


FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across file
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    for _,_,filenames in os.walk(directory):

      data = {}
      for file in filenames:
        with open(os.path.join(directory,file)) as f:
          data[file] = f.read()

    return data


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    tokens = nltk.tokenize.word_tokenize(document)

    filter_string = string.punctuation

    # Catch repeated characters
    for char in string.punctuation:
      filter_string += char * 5

    filter_string += "'s"
    
    filtered_tokens = []
    for token in tokens:

      if token in filter_string:
        # catch puncutation and repeated characters
        continue
      if token in nltk.corpus.stopwords.words("english"):
        continue
      else:
        filtered_tokens.append(token.lower())

    return(filtered_tokens)


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    total_documents = len(documents.keys())

    print(total_documents)

    idfs = {}

    appears_in = {}

    counters = {}

    # Want to do this for each word in each document
    
    for document in documents.keys():
      counters[document] = Counter(documents[document])

      # print(counters[document])

    # Now we have a counter for word frequency for each document
      
    for document, counter in counters.items():
      for word in counter:
        try:
          appears_in[word].append(document) 
        except KeyError:
          appears_in[word] = [document]

    # TODO: appears_in is not accurately counting



    for word in appears_in:
      num_documents_containing_word = len(appears_in[word]) 
      idfs[word] = math.log(total_documents / num_documents_containing_word) 

    # testing
    for word in appears_in: 
      if len(appears_in[word]) >3:
        print(word)
        print(idfs[word])

    return idfs


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    raise NotImplementedError


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    raise NotImplementedError


if __name__ == "__main__":
    main()

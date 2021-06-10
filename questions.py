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
        with open(os.path.join(directory,file), encoding="utf8") as f:
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

      # TODO: 'the' is still getting through

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

    
    for document in documents.keys():
      counters[document] = Counter(documents[document])
      print(counters[document])

    # Now we have a counter for word frequency for each document
      

    for document, counter in counters.items():
      for word in counter:
        try:
          appears_in[word].append(document) 
        except KeyError:
          appears_in[word] = [document]


    for word in appears_in:
      num_documents_containing_word = len(appears_in[word]) 
      idfs[word] = math.log(total_documents / num_documents_containing_word) 


    return idfs


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    print(query)
    print(nltk.corpus.stopwords.words("english"))

    counters = {}
    for file in files:
      counters[file] = Counter(files[file])

    
    tf_idf_sums = {}

    
    for file in files:
      print(file)
      tf_idf_sums[file] = 0

      for word in query:
        

        if word not in files[file]:
          continue
        else:
          print(word)
          tf = counters[file][word]
          idf = idfs[word]
          tf_idf = tf * idf
          print(tf_idf)
          tf_idf_sums[file] += tf_idf

    tf_idf_list = list(tf_idf_sums.items())

    print(tf_idf_list)

    tf_idf_list = sorted(tf_idf_list, key=lambda x: x[1], reverse=True)
    print(tf_idf_list)

    to_return = [pair[0] for pair in tf_idf_list[0:n]]
    print(to_return)

    return [pair[0] for pair in tf_idf_list[0:n]]




    


    # The returned list of filenames should be of length n and should be ordered with the best match first.

    # Recall that tf-idf for a term is computed by multiplying the number of times the term appears in the document by the IDF value for that term.

    # Files should be ranked according to the sum of tf-idf values for any word in the query that also appears in the file. 
    # Words in the query that do not appear in the file should not contribute to the file’s score.
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

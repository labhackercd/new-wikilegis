from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from nltk.corpus import stopwords
from nltk import word_tokenize
from nltk.stem import RSLPStemmer
from string import punctuation
from kneed.knee_locator import KneeLocator
from scipy.spatial.distance import cdist
import numpy as np
from collections import defaultdict


def process_text(text, stem=True):
    """ Tokenize text and stem words removing punctuation and numbers """
    text = text.translate(str.maketrans('', '', punctuation))
    text = text.translate(str.maketrans('', '', '1234567890'))

    tokens = word_tokenize(text)

    if stem:
        stemmer = RSLPStemmer()
        tokens = [stemmer.stem(t) for t in tokens]

    return tokens


def clustering_suggestions(suggestions, n_clusters=None):
    vectorizer = TfidfVectorizer(stop_words=stopwords.words('portuguese'),
                                 tokenizer=process_text,
                                 use_idf=True,
                                 max_df=0.9,
                                 min_df=0.01,
                                 ngram_range=(1, 2),
                                 lowercase=True)

    X = vectorizer.fit_transform(suggestions.values_list('content', flat=True))

    if n_clusters:
        model = KMeans(n_clusters=n_clusters, init='k-means++', max_iter=100,
                       n_init=1)
    else:
        distortions = []
        max_k = len(suggestions) - 1
        K = range(2, max_k)
        for k in K:
            kmeanModel = KMeans(n_clusters=k)
            kmeanModel.fit_transform(X)
            distortions.append(
                sum(np.min(cdist(X.toarray(),
                                 kmeanModel.cluster_centers_,
                                 'euclidean'), axis=1)) / X.shape[0])

        kn = KneeLocator(
            K, distortions, curve='convex', direction='decreasing')

        true_k = kn.knee
        model = KMeans(
            n_clusters=true_k, init='k-means++', max_iter=100, n_init=1)

    model.fit_transform(X)

    suggestions_list = []

    for suggestion in suggestions:
        Y = vectorizer.transform([suggestion.content])
        prediction = model.predict(Y)
        suggestions_list.append((
            suggestion.id,
            prediction[0]
        ))

    clusters = defaultdict(list)

    for suggestion, cluster in suggestions_list:
        clusters[cluster].append(suggestion)

    clusters_list = list(clusters.values())

    return clusters_list

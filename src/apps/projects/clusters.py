from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from nltk.corpus import stopwords as nltk_stopwords
from string import punctuation
from kneed.knee_locator import KneeLocator
from scipy.spatial.distance import cdist
import numpy as np


def clustering_suggestions(suggestions, n_clusters=None):
    stopwords = nltk_stopwords.words('portuguese') + list(punctuation)
    vectorizer = TfidfVectorizer(stop_words=stopwords,
                                 smooth_idf=True,
                                 analyzer='word',
                                 token_pattern=r'\w{2,}',
                                 ngram_range=(1, 2),
                                 max_features=30000)

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

    clusters = []

    for suggestion in suggestions:
        Y = vectorizer.transform([suggestion.content])
        prediction = model.predict(Y)
        clusters.append({
            'suggestion': suggestion,
            'cluster': prediction[0]
        })

    return clusters

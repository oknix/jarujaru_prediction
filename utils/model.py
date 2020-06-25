import numpy as np

class _BaseNB:
    def __init__(self, alpha=1.0, beta=1.0, theta_c=None, phi_cv=None):
        """
        :param alpha: smoothing param for calculating each category's prior distribution (default: Laplace smoothing)
        :param beta: smoothing param for calculating the probability of category c choosing the word v
        (default: Laplase smoothing)
        :param theta_c: category c's prior distribution
        :param phi_cv: the probability of category c selecting the word v
        """
        self.alpha = alpha
        self.beta = beta
        self.theta_c = theta_c
        self.phi_cv = phi_cv

class tBernoulliNB(_BaseNB):

    def fit(self, x, y):
        n_documents, vocabulary_size = x.shape
        n_categories = len(set(y))
        categories = sorted(list(set(y)))

        if self.theta_c is None:
            self.theta_c = np.zeros(shape=(n_categories, 1), dtype=np.float32)

        if self.phi_cv is None:
            self.phi_cv = np.zeros(shape=(n_categories, vocabulary_size), dtype=np.float32)

        for i, category in enumerate(categories):
            lc = np.sum(y == category)
            self.theta_c[i] = (lc + self.alpha) / (n_documents + n_categories * self.alpha)

            c_docs = x[y == category]
            mc = np.sum(c_docs, axis=0)
            self.phi_cv[i] = (mc + self.beta) / (lc + 2. * self.beta)

    def predict(self, x):
        log_likelihood = np.dot(np.log(self.phi_cv), x.T) + np.dot(np.log(1. - self.phi_cv), (1. - x).T)
        y = np.argmax(np.log(self.theta_c) + log_likelihood, axis=0)
        return y

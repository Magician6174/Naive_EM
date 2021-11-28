"""Mixture model using EM"""
from typing import Tuple
import numpy as np
from utils import GaussianMixture


def estep(X: np.ndarray, mixture: GaussianMixture) -> Tuple[np.ndarray, float]:
    """E-step: Softly assigns each datapoint to a gaussian component

    Args:
        X: (n, d) array holding the data
        mixture: the current gaussian mixture

    Returns:
        np.ndarray: (n, K) array holding the soft counts
            for all components for all examples
        float: log-likelihood of the assignment
    """

    n, d = X.shape
    K, _ = mixture.mu.shape
    post = np.zeros((n, K))
    dr = np.sqrt((2*np.pi*mixture.var)**d)
    exponent_nr = -0.5*(np.linalg.norm(X[:,:,None] - mixture.mu.T,axis=1)**2)
    normal_ = np.exp(exponent_nr/mixture.var)/dr
    log_likelihood = np.sum(np.log(np.sum(mixture.p*normal_,axis=1)))
    post = (mixture.p*normal_)/(np.sum(mixture.p*normal_,axis=1,keepdims=True))

    return post, log_likelihood
    


def mstep(X: np.ndarray, post: np.ndarray) -> GaussianMixture:
    """M-step: Updates the gaussian mixture by maximizing the log-likelihood
    of the weighted dataset

    Args:
        X: (n, d) array holding the data
        post: (n, K) array holding the soft counts
            for all components for all examples

    Returns:
        GaussianMixture: the new gaussian mixture
    """

    n, d = X.shape
    _, K = post.shape
    n_hat = post.sum(axis=0, keepdims=True)
    p = n_hat / n
    mu = np.zeros((K, d))
    var = np.zeros(K)
    mu = post.T @ X / n_hat.T
    var = np.sum(post * (np.linalg.norm(X[:,:,None] - mu.T,axis=1)**2),axis=0)/(d*n_hat)

    return GaussianMixture(mu, var[0], p[0])


def run(X: np.ndarray, mixture: GaussianMixture,
        post: np.ndarray) -> Tuple[GaussianMixture, np.ndarray, float]:
    """Runs the mixture model

    Args:
        X: (n, d) array holding the data
        post: (n, K) array holding the soft counts
            for all components for all examples

    Returns:
        GaussianMixture: the new gaussian mixture
        np.ndarray: (n, K) array holding the soft counts
            for all components for all examples
        float: log-likelihood of the current assignment
    """
    prev_cost = None
    cost = None
    while True:
        prev_cost = cost
        post, cost = estep(X, mixture)
        mixture = mstep(X, post)
        try:
            if (abs(prev_cost - cost) < (1e-6*np.abs(cost))):
                break
            else:
                continue        
        except:
            pass
    return mixture, post, cost


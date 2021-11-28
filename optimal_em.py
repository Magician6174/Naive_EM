import numpy as np
import utils
import utils
import naive_em

def run_with_bic(X):
    """
    Plot the mixture model for 2D dataset with optimal number of parameters
    
    Args:
        X: (n,d) array holding data
    """
    bic_max = None
    best_K = None
    for K in range(1,5):
        best_seed = None
        max_likelihood = None

        for seed in range(0,5):
            mixture, post = utils.initialize(X,K,seed)
            mixture, post, log_likelihood = naive_em.run(X,mixture, post)

            if max_likelihood is None or log_likelihood>max_likelihood:
                max_likelihood = log_likelihood
                best_seed = seed
        
        mixture, post = utils.initialize(X,K,best_seed)
        mixture, post, log_likelihood = naive_em.run(X,mixture, post)
        bic = utils.bic(X,mixture,log_likelihood)

        if bic_max is None or bic > bic_max:
            bic_max = bic
            best_K = K
    return best_K, best_seed

    

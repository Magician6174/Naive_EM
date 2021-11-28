import numpy as np
import utils
import naive_em
import optimal_em

X = np.loadtxt("toy_data.txt")

seeds = [0,1,2,3,4]

K = [1,2,3,4] # Number of Clusters

WITH_BIC = True

if WITH_BIC:
    best_K, best_seed = optimal_em.run_with_bic(X)
    mixture, post = utils.initialize(X,best_K,best_seed)
    mixture,post,log_likelihood = naive_em.run(X,mixture,post)
    utils.plot(X,mixture,post,f"EM with K={best_K}")
else:
    K = np.random.choice(K)
    seed = np.random.choice(seeds)
    mixture, post = utils.initialize(X,K,seed)
    mixture,post,log_likelihood = naive_em.run(X,mixture,post)
    utils.plot(X,mixture,post,f"EM with K={K}")

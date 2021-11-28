import numpy as np
import utils
import kmeans

X = np.loadtxt("toy_data.txt")

seeds = [0,1,2,3,4]

K = [1,2,3,4] # Number of Clusters

K = np.random.choice(K)
seed = np.random.choice(seeds)
mixture, post = utils.initialize(X,K,seed)
mixture,post,log_likelihood = kmeans.run(X,mixture,post)
utils.plot(X,mixture,post,f"Kmeans Clustering with K={K}")
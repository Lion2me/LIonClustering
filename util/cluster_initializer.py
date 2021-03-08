import scipy
import numpy as np
from cluster.cluster_ import cluster_
import scipy.sparse as sc_sparse


def calMaximumEntropy(self,cluster_count):
    # 더 좋은 방법이 있다면...
    return scipy.stats.entropy([1 for i in range(cluster_count)])

def np_random_initialize(self,data,n_range,n_shape):
    init_cluster_vector_index = np.random.randint(low=n_range[0],high=n_range[1],size=n_shape)
    init_cluster_vector = [data[i] for i in init_cluster_vector_index ]
    clusters = [cluster_(i,n_range[1],init_cluster_vector[i]) for i in range(n_shape[0])]

    return clusters


def entropy_based_initialize(self,data,n_range,n_shape,dist_func,n_iter=10):

    max_entropy = calMaximumEntropy(n_shape[0])

    entropy_score = 0

    result_clusters = 0

    for iterate in range(n_iter):

        init_cluster_vector_index = np.random.randint(low=n_range[0],high=n_range[1],size=n_shape)
        init_cluster_vector = [data[i] for i in init_cluster_vector_index ]

        clusters = [cluster_(i,n_range[1],init_cluster_vector[i]) for i in range(n_shape[0])]

        cluster_vectors = sc_sparse.vstack([i.get_centroid() for i in clusters])
        # 한번에 거리 계산
        close_cluster = dist_func(cluster_vectors,data)

        close_idx = np.argmin(close_cluster.T,axis=1)
        print(data[close_idx==0].shape)

        cluster_entropy_score = scipy.stats.entropy([data[close_idx==cix].shape[0] for cix in range(n_shape[0])]) / max_entropy

        if cluster_entropy_score > entropy_score:
            entropy_score = cluster_entropy_score
            result_clusters = clusters

    return result_clusters

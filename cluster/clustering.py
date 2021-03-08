
from util.distance import distance
from util.cluster_initializer import np_random_initialize , entropy_based_initialize
import numpy as np
import scipy
import scipy.stats as sc
import scipy.sparse as sc_sparse

class clustering:

    def __init__(self,cluster_num=20,max_iter=5,dist_func='cos',initialize='random',stop_rate = 1000):
        # 이후에 라이브러리 형식으로 변환
        distance_class = distance()
        self.cluster_num = cluster_num
        self.max_iter = max_iter
        self.stop_rate = stop_rate
        self.stop_entropy = np.inf
        self.initialize = initialize
        if(dist_func == 'cos'):
            self.dist_func = distance_class.cosine_distance
        elif(dist_func == 'euc'):
            self.dist_func = distance_class.euclidean_distance
        elif(dist_func == 'jac'):
            self.dist_func = distance_class.jaccard_distance
        elif(dist_func == 'pearson'):
            self.dist_func = distance_class.pearson_distance
        elif(dist_func == 'KL'):
            self.dist_func = distance_class.KL_diver
        else:
            print('Cos / Euc / Jac / Pearson / Kl-Diver 중 하나의 거리를 고르세요')

    def init_cluster(self):
        self.cluster_vector = [[] * i for i in range(self.cluster_num)]

    # data = Count Vecters or TF-IDF Vectors shape
    def fit(self,data):
        cluster_size = data.shape[0]
        self.stop_rate = 0

        if(self.initialize == 'random'):
            self.clusters = np_random_initialize(data,n_range=[0,cluster_size],n_shape=[self.cluster_num])
        if(self.initialize == 'entropy'):
            self.clusters = entropy_based_initialize(data,n_range=[0,cluster_size],n_shape=[self.cluster_num],dist_func=self.dist_func)
        else:
            print('initialize error')

        preq_cluster_vector = []
        preq_entropy = np.inf;

        for i in range(self.max_iter):
            print('iter = ',i)

            cluster_vectors = sc_sparse.vstack([i.get_centroid() for i in self.clusters])
            # 한번에 거리 계산
            close_cluster = self.dist_func(cluster_vectors,data)

            close_idx = np.argmin(close_cluster.T,axis=1)

            prev_entropy = sc.entropy([cluster.cluster_num for cluster in self.clusters])

            for j in range(20):
                if(data[close_idx==j].shape[0] > 0):
                    self.clusters[j].set_centroid_(sc_sparse.csr_matrix(scipy.mean(data[close_idx==j],axis=0)))
                    self.clusters[j].set_cluster_num(data[close_idx==j].shape[0])

            now_entropy = sc.entropy([cluster.cluster_num for cluster in self.clusters])

            if i == 1:
                if self.stop_rate != 0:
                    self.stop_entropy = (now_entropy - prev_entropy) / self.stop_rate
                if self.stop_rate == 0:
                    self.stop_entropy = 0

            elif(self.stop_entropy != np.inf and np.abs(now_entropy - prev_entropy) <= self.stop_entropy):
                break

import scipy.sparse as sc_sparse

class cluster_:
    
    def __init__(self,cid,d_length,init_vector):
        self.clusterid_ = cid
        self.cluster_count_ = 1
        self.cluster_num = 0
        self.centroid_ = init_vector
        
    def get_centroid(self):
        return self.centroid_
    
    def get_clusterid(self):
        return self.clusterid_
        
    def clear_cluster_list(self):
        self.cluster_list_ = sc_sparse.csr_matrix(self.centroid_)
        self.cluster_list_index = []
    
    def set_centroid_(self,centroid):
        self.centroid_ = centroid
    
    def set_cluster_num(self,cluster_num):
        self.cluster_num = cluster_num
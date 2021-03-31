from scipy.spatial import distance as scidist
from sklearn.metrics import pairwise_distances
from scipy import stats as sc

class distance:
    
    def cosine_distance(self,source,target):
        return pairwise_distances(source,target,metric='cosine')
                    
    def euclidean_distance(self,source,target):
        return pairwise_distances(source,target,metric='euclidean')
        
    def jaccard_distance(self,source,target):
        return pairwise_distances(source,target,metric='jaccard')
    
    def pearson_distance(self,source,target):
        return pairwise_distances(source,target,metric='correlation')
    
    # KL_diver를 계산할 때 target의 데이터의 평균과 분산을 바탕으로 source를 정규분포로 바꾸어 계산해야 하는가? - 단어라 안될 듯
    
    def KL_diver(self,source,target):
        
        source_dist = sc.entropy(source,target)
        target_dist = sc.entropy(target,source)
        
        dist = (source_dist + target_dist) / 2
                
        return dist
        #return np.sum((source/(source+target))*source*np.log(source/target)) + np.sum((target/(source+target))*target*np.log(target/source))
    

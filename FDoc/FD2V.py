import fasttext
import numpy as np
import os
import heapq
from sklearn.metrics import pairwise_distances
from gensim.models.doc2vec import TaggedDocument
from sklearn.neighbors import NearestNeighbors

class fd2v():

    def __init__(self,model_path = './lionlp_fast_model.bin'):
        # docs는 문자열? 딕셔너리? taggedocument 형태로
        self.docs = []
        # docs를 모델로 바꾸는 것도 만들어야 할 듯
        if(os.path.exists(model_path)):
            self.model = fasttext.load_model(model_path)
        else:
            self.model = None
        self.doc_vecs = False
        self.dim = self.model.get_word_vector('가').shape[0]

    def get_document_vector(self,text):
        return np.array([self.model.get_word_vector(x) for x in text.split(' ')]).mean(axis=0)

    def get_document_vectors(self, texts):
        all_vector = []
        for idx , text in enumerate(texts):
            if(type(text) != str):
                continue
            all_vector.append(np.array([self.model.get_word_vector(x) for x in text.split(' ')]).mean(axis=0))
        return all_vector

    def get_document_vectors_from_words(self, texts):
        all_vector = []
        for idx , text in enumerate(texts):
            vec = np.array([self.model.get_word_vector(x) for x in text]).mean(axis=0)
            if (type(text) != str or vec.shape == ()):
                print(text)
                continue
#            all_vector.append(np.array([self.model.get_word_vector(x) for x in text]).mean(axis=0))
            all_vector.append(vec)
        return np.array(all_vector)

    def get_word_vectors(self,text):
        return np.array([self.model.get_word_vector(x) for x in text.split(' ')])

    def fit(self, docs):
        # tag별로 묶어서?
        if(type(self.model) == fasttext.FastText._FastText):
            self.doc_vecs = self.get_document_vectors_from_words(docs)
        else:
            print("추후에 문장을 단어 및 자모로 변환하고 파일을 빼는 것 필요")
            print("실제로 모델을 만드는 과정 - 모든 파라미터는 사용 할 수 있도록 하자")

    # 추후에 knn알고리즘의 세부 설정은 지정하자 ( 2021 - 03 - 11 )
    def fit_knn_docs(self,N=10,dist_func = 'cosine'):
        self.nbrs = NearestNeighbors(n_neighbors=N, metric=dist_func).fit(self.doc_vecs)

    def get_knn_docs(self,text):
        distances, indices = self.nbrs.kneighbors(self.get_document_vector(text).reshape(1,-1))
        return {'distance' : distances , 'indices' : indices}

    def get_similar_key_docs(self,X,Y,N=10,dist_func = 'cosine'):
        #아래의 공식의 값을 max_heap에 넣으면 됨 maxheap의 크기는 N을 입력받고 ㄱㄱ
        #np.min(fd2v.get_similar_key_docs(input_,'ㅊㅓㅇㄴㅕㄴㅇㅡㄴ ㅇㅓㄷㅣㅇㅔㅅㅓ ㅇㅣㄹㅎㅏㄴㅏㅇㅛ'), axis=1).sum()
        heap = []

        for idx,text in enumerate(Y):
            dist = np.min(pairwise_distances(self.get_word_vectors(X),self.get_word_vectors(text),metric = dist_func),axis=1).sum()
            if(len(heap) < N):
                heapq.heappush(heap,(-dist,dist,idx))
            elif(dist < heap[0][1]):
                heapq.heappop(heap)
                heapq.heappush(heap,(-dist,dist,idx))
        return heap
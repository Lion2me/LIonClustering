import fasttext
import numpy as np
import os
from sklearn.metrics import pairwise_distances
from gensim.models.doc2vec import TaggedDocument

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
            all_vector.append(np.array([self.model.get_word_vector(x) for x in text.split(' ')]).mean(axis=0))
        return all_vector

    def get_document_vectors_from_words(self, texts):
        all_vector = []
        for idx , text in enumerate(texts):
            all_vector.append(np.array([self.model.get_word_vector(x) for x in text]).mean(axis=0))
        return all_vector

    def fit(self, docs):
        # tag별로 묶어서?
        if(type(self.model) == fasttext.FastText._FastText and type(docs) == TaggedDocument):
            self.docs = docs
            self.doc_vecs = self.get_document_vectors_from_words([text.words for text in docs])
        else:
            print("추후에 문장을 단어 및 자모로 변환하고 파일을 빼는 것 필요")
            print("실제로 모델을 만드는 과정 - 모든 파라미터는 사용 할 수 있도록 하자")


    def get_similar_docs_index(self,text,N = 10,dist_func = 'cosine'):
        # type으로
        if self.doc_vecs == False:
            raise Exception('please Fitting first')
        else:
            dist = pairwise_distances(self.get_document_vector(text).reshape(-1,self.dim),self.doc_vecs,metric=dist_func).reshape(-1).argsort()
            return np.where(dist<N)

    def get_similar_docs(self,text,N=10,dist_func = 'cosine'):
        if self.doc_vecs == False:
            raise Exception('please Fitting first')
        else:
            return [' '.join(self.docs.words[idx]) for idx in self.get_similar_docs_index(text,N,dist_func)]
            #for idx in np.where(dist<N):
            #    yield self.docs.words[idx]



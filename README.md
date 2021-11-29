## Lion2me의 NLP 공부 라이브러리입니다.

Jupyter notebook 환경에서 진행 후 올리므로 최적화까지 시간이 걸립니다.

1. Clustering [ K-Means ]

K-Means 클러스터링을 구현해보았습니다.

K-Means의 경우 Distance를 계산하는 방식에 따라 효과가 달라짐을 볼 수 있습니다. 현재까지 Cosine , Euclidean , corr , jaccard 방식이 구현되었습니다. 추후에 확률분포의 차이를 구하는 KL-Divergence 를 이용해 볼 예정입니다.

논문에서는 KL-Divergence의 스케일을 잘 적용했지만, 저는 아직 부족한 점이 있어서 그 부분은 차차 넓혀보겠습니다.

```python
clus = clustering()

CV = CountVectorizer()
TV = TfidfTransformer()

CVmodel = CV.fit_transform(test)
TVmodel = TV.fit_transform(CVmodel)

clus.fit(data = TVmodel)

clus.clusters[0].get_centroid()
```


2. FastText Doc2Vec

정확한 Doc2Vec 진행 방식이 아닙니다. 여기서 문장의 벡터는 등장하는 단어 벡터의 평균으로 진행했습니다.

방식은 FastText를 통해 해당 문장의 단어 벡터들의 평균을 구한 뒤 저장합니다.

```python

# 여기서 model_path는 FastText를 통해 얻어진 모델입니다.
model = fd2v(model_path = './petitions_word_model.bin')

# fit을 통해 각 문장에 대한 벡터를 구합니다.
# 문장에 대한 벡터는 등장 단어 벡터의 평균입니다.
model.fit(petitions_text)
```

fit을 마치면 모든 문장의 벡터가 들어있기 때문에 원하는 작업을 진행 할 수 있습니다.

```python
input_= '청소년'
model.model.get_nearest_neighbors(input_)

-------------------------------

[(0.9044303894042969, '청소년및'),
 (0.8942788243293762, '청소년폭력'),
 (0.8893114328384399, '청소년용'),
 (0.8861926794052124, '청소년대상'),
 (0.8856853246688843, '청소년용과'),
 (0.8692178726196289, '청소년일'),
 (0.8685765862464905, '청소년'),
 (0.8658358454704285, '청소년증'),
 (0.8623796105384827, '청소년등'),
 (0.8612908720970154, '청소년보호')]
```

입력했던 FastText 모델은 model의 이름으로 입력되어 있으므로 사용할 수 있습니다.

```python
model.fit_knn_docs()
```

fit_knn_docs는 sklearn의 KNN을 사용했습니다.

저장 된 문장 벡터를 기반으로 knn 모델을 만듭니다. 이 과정에서 파라미터를 정할 수 있도록 변경하도록 하겠습니다.

```python
input_ = "청소년들의 범죄"
model.get_knn_docs(input_)

{'distance': array([[0.41203612, 0.42030394, 0.4212376 , 0.42178512, 0.4224677 ,
         0.42316353, 0.43128324, 0.43642706, 0.43715572, 0.43752843]],
       dtype=float32),
 'indices': array([[ 79739,  63776, 116940,  22991,  87623, 102335,  22952, 187072,
          18268, 116996]])}
```

추가적으로 단어를 기반으로 해당 단어와 유사한 단어가 등장하는 모델을 만들어 보았습니다. 데이터 전체를 탐색하며 연산하므로 시간이 매우 느립니다만, 키워드를 기반으로 탐색하는 방법으로 꽤 괜찮은 결과가 나왔습니다.

```python
model.get_similar_key_docs(input_,petitions_text)


# 첫번째 값은 max heap의 사용때문에 넣었습니다.
[(-0.53092664, 0.53092664, 223587),
 (-0.52915925, 0.52915925, 300356),
 (-0.47592646, 0.47592646, 64489),
 (-0.5158793, 0.5158793, 90852),
 (-0.4864934, 0.4864934, 364480),
 (-0.3284487, 0.3284487, 2655),
 (-0.46308434, 0.46308434, 244445),
 (-0.51326764, 0.51326764, 273069),
 (-0.45213115, 0.45213115, 299748),
 (-0.47793502, 0.47793502, 391832)]

```

이 기능을 이용해서 두 문장의 등장 단어 전체를 비교해서 나온 유사도를 평균을 리턴해주는 함수를 만들어보았습니다.

```python
# X - STRING
# Y - STRING LIST

def get_similar_key_docs_score(self,X,Y,N=10,dist_func = 'cosine'):

    score = 0
    for idx,text in enumerate(Y):
        dist = np.min(pairwise_distances(self.get_word_vectors(X),self.get_word_vectors(text),metric = dist_func),axis=1).sum()
        score += dist

    return score/len(Y)
    
4.156350175539653

```

화장품 관련 커뮤니티를 약간 크롤링해서 어떤 방식으로 사용 할 수 있는지 예제를 만들어보았습니다.
글로우픽이라는 화장품 리뷰 데이터와 상품 설명 데이터를 수집하여 다음과 같은 서비스를 만들어보았습니다.

```python
from util.tagging import tagging
from FDoc.fd2v import fd2v

tag = tagging()

# cc.ko.300.bin은 위키피디아 정보로 만들어진 Pretrained FastText입니다.
model = fd2v('../data/cc.ko.300.bin')

sent = ['기초부터 피부를 탄탄하게 다져주어 피부결을 부드럽고 촉촉하게 도와주는 에센스 토너']
sent = tag.get_pos(sent,pos=POS,result_type = 'str')
print(sent)
# 결과는 '기초 피부 탄탄 주 부결 부드럽 촉촉 주 에센스 토너'

scores = [ ( item_df['brand'][i] ,item_df['product'][i], model.get_similar_key_docs_score(sent[0],item_df['review'][i]+item_df['desc'][i]+ [item_df['product'][i]] ) ) for i in range(len(item_df)) ]
scores = sorted(scores, key=lambda x:x[2])

#[('루트리 (ROOTREE)', '피토 그라운드 딥 컴포트 크림 토너', 4.156350175539653),
# ('스킨알엑스랩 (SKINRx LAB)', '더블 에센스 토너', 4.212137651443482),
# ('쁘띠페 (PETITFEE)', '에너지 앰플 패드', 4.240628549030849),
# ('라포티셀 (LAPOTHICELL)', '오일 컷 클레이 로션', 4.2827998995780945),
# ('노멀노모어 (NORMAL NOMORE)', '안티 드라이 인텐시브 토너', 4.314711830832741),
# ('펠드아포테케 (Feld apotheke)', '이뮨셀 트리트먼트', 4.403622309366862),
# ('이네이처 (E nature)', '버치 주스 하이드로 에센스 스킨', 4.468891962980613),
# ('라곰 (LAGOM)', '셀러스 리바이브 에센 토너', 4.480025457172859),
# ('땡큐파머(THANK YOU FARMER)', '강화 교동쌀 맑음 에센셜 토너', 4.486284136772156),
# ('BRTC (비알티씨)', '더 퍼스트 앰플 에센스', 4.503092235209895),
# ...
```

리뷰 정보를 기반으로 입력 한 문장에 관련해서 가장 가까운 리뷰 및 상품 정보를 얻을 수 있습니다.
하지만 이 알고리즘의 동작 속도가 매우 느리기 때문에 중간 정보를 이용해서 학습을 유지하는 방향으로 동작하면 더 좋을 것 같습니다.


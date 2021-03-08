from konlpy.tag import Mecab

class tagging:
    
    def __init__(self,user_words = ''):
        self.mecab = Mecab()
        
    def get_pos(self,sents,pos='all',result_type = 'list'):
        
        if( pos == 'all' ):
            for i,sent in enumerate(sents):
                sents[i] = [word for word,pos_ in self.mecab.pos(sent)]
        else:
            for i,sent in enumerate(sents):
                try:
                    sents[i] = [word for word,pos_ in self.mecab.pos(sent) if pos_ in pos ]
                except:
                    sents[i] = ['error']
        if(result_type == 'list'):
            return sents
        elif(result_type == 'str'):
            return list(map( lambda x:' '.join(x),sents))
        else:
            return 'error'
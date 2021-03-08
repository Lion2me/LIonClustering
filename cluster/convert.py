class convert:
    
    def __self__(self):
        print('Convert')
        
        
    '''
    Convert DataSet
    
    use dictionary for calculate cost
    so all of data(pandas DataFrame) convert to dictionary
    '''
    def convert_index_data(self,source):
        return dict(zip(source.indices,source.data))
    '''
    Convert_vector function
    
    make two dict( shape = {index, value} ) to list of comparable shape
    '''
    def convert_vector(self,source,target,distF='cos'):
        col = set(source.keys()).union(set(target.keys()))
        if(distF == 'KL'):
            temp_a = defaultdict(float,dict(list(map(lambda x:(x,1e-5),col))))
            temp_b = defaultdict(float,dict(list(map(lambda x:(x,1e-5),col))))
        else:
            temp_a = defaultdict(float,dict(list(map(lambda x:(x,0),col))))
            temp_b = defaultdict(float,dict(list(map(lambda x:(x,0),col))))
        temp_a.update(source)
        temp_b.update(target)
        return (np.array(list(temp_a.values())),np.array(list(temp_b.values())))

    '''
    jaccard distance is so simple calculation
    
    just we need to know how many equivalent element and different element
    so we can calculate jaccard distance
    
    '''
    def convert_jaccard(self,source,target):
        a = set(source.keys())
        b = set(target.keys())
        
        return len(a&b)/len(a|b)
        
    def calulate_mean(self,source):
        return np.mean(source)

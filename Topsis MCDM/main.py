
from check import topsis
import pandas as pd
from topsis import tops
    
dataset = pd.read_csv('data.csv')
dt = pd.read_csv('data.csv')
dataset = dataset.iloc[:,:-3].values
print(dataset)
c = [1,1,1,1,1,1,1,1,1]
impact = [0,1,1,1,1,1,1,1,1]
#p = tops(dataset,impact,c)
p=topsis(dataset,c,impact)


#p.calc()
#print(p)


import numpy as np
from check import topsis
import pandas as pd
from topsis import tops


def weights(df):
  y=[]
  print(1)  
  for j in range(10):
    y.append(list(df.iloc[j,1:]))
  print(y)  
  criteria_matrix = np.array(y)
  #print(criteria_matrix)

  # Column Sum
  col_sum = criteria_matrix.sum(axis=0)

  # Normalised Criteria Matrix
  normalised_criteria_matrix = criteria_matrix / col_sum

  # We calculate the eighen vector
  eighen_vector = normalised_criteria_matrix.mean(1)

  eighen_vector =  np.reshape(eighen_vector, (1, 10))
  print(eighen_vector)
  return eighen_vector[0][:9] 


def runMain(df):    
  dataset = pd.read_csv('data.csv')
  dt = pd.read_csv('data.csv')
  dataset = dataset.iloc[:,:-3].values
  #print(dataset)
  print(3)
  #c = [1,1,1,1,1,1,1,1,1]
  
  c=weights(df)
  print(c)
  impact = [0,1,1,1,1,1,1,1,1]
  #p = tops(dataset,impact,c)
  p=topsis(dataset,c,impact)
  y=p.calc()
  df={"Node":["Node "+str(i+1) for i in range(len(y))],"Results":y}
  maximum=max(y)
  node=y.index(maximum)+1  
  return [df,node,maximum]
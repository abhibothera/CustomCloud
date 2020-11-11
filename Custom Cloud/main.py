import numpy as np
from check import topsis
import pandas as pd
from sklearn.preprocessing import MinMaxScaler  
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import numpy as np
import pandas as pd
from mcdm import executors as exe

#impact
impact = [0,1,1,1,1,1,1,0,1]

#Takes original data of data provider, result of MCDM Avg
def predict(data,y):
  scaler = MinMaxScaler(feature_range=(0,1))  
  scaled_data = scaler.fit_transform(data)
  X_train, X_test, Y_train, Y_test = train_test_split(scaled_data, y, test_size=0.2,shuffle=False)
  clf = RandomForestRegressor()
  clf.fit(X_train, Y_train)
  prediction = (clf.predict(X_test))
  for i in range(len(prediction)):
    print(Y_test[i],prediction[i])

#Takes in dataframe
def weights(df):
  y=[]
  #Iterate through 9 rows (As weight matrix has 9 parameters) 
  for j in range(10):
    y.append(list(df.iloc[j,1:]))

  criteria_matrix = np.array(y)
  #print(criteria_matrix)

  # Column Sum
  col_sum = criteria_matrix.sum(axis=0)

  # Normalised Criteria Matrix
  normalised_criteria_matrix = criteria_matrix / col_sum

  # We calculate the eighen vector
  eighen_vector = normalised_criteria_matrix.mean(1)

  eighen_vector =  np.reshape(eighen_vector, (1, 10))
  #print(eighen_vector)
  return eighen_vector[0][:9] 

#Takes in dataframe
def runMain(df):
  #Read excel file as a dataframe
  dataset = pd.read_csv('data.csv')

  #Selective column inputs 
  colnames=[i for i in dataset][:-3]
  #Generating new dataframe from Selective columns
  new_df=dataset[colnames]
  dataset = dataset.iloc[:,:-3].values
  #Weights
  w=weights(df)
  #Impact Factor (Positive or Negative)
  
  #Topsis
  #top=topsis(dataset,w,impact)
  #y=top.calc()
  #Dictionary to store performance against each data nnode of provider.
  #df={"Node":["Node "+str(i+1) for i in range(len(y))],"Results":y}

  #new_df['Y']=y
  #return [new_df,y]


  #Input File (Data of Service Provider)
  #dataset-> User entered weight matrix
  #df=pd.read_excel("input.xlsx")


  #out=runMain(df)
  #print(predict(out[0],out[1]))





  #dataset = pd.read_csv('data.csv')
  #dataset = dataset.iloc[:,:-3].values
  matrix=[]

  for i in range(len(dataset)):
    matrix.append(list(dataset[i]))

  inputs=pd.read_csv('data.csv')
  #criteria
  colname=[chr(i) for i in range(65,74)]
  alts=['A'+str(i) for i in range(1,len(inputs)+1)]
  w1=weights(df)
  impact = [0,1,1,1,1,1,1,1,1]
  impact=[bool(j) for j in impact]


  xij = pd.DataFrame(matrix, index=alts, columns=colname)

  kwargs = {
      'data': xij,
      'beneficial': impact,
      'weights': w1,
      'rank_reverse': True,
      'rank_method': "ordinal"
  }

  #MCDM Executor
  wsm = exe.WSM(**kwargs) # Weighted Sum Method
  topsis = exe.Topsis(**kwargs) # Topsis 
  vikor = exe.Vikor(**kwargs) # Vikor 




  # show results
  print("WSM Ranks")
  print(wsm.dataframe)

  print("TOPSIS Ranks")
  print(topsis.dataframe)

  print("Vikor Ranks")
  print(vikor.dataframe)


  # How to choose best MCDM Method ?

  # Instantiate Rank Analizer
  analizer = exe.RankSimilarityAnalyzer()

  # Add MCDMs to anlizer
  analizer.add_executor(wsm)
  analizer.add_executor(topsis)
  analizer.add_executor(vikor)

  # run analizer
  results = analizer.analyze()
  print(results)




  def avg(x,y,z):
    r=pow((0.2*(x**2))+(0.3*(y**2))+(0.5*((1-z)**2)),0.5)
    return r

  # show results
  df={"WSM":[],"TOPSIS":[],"VIKOR":[]}
  df["WSM"]=list(wsm.dataframe['RATE'])
  df["TOPSIS"]=list(topsis.dataframe['RATE'])
  df["VIKOR"]=list(vikor.dataframe['RATE'])
  df=pd.DataFrame(df)
  x=list(df['WSM'])
  y=list(df['TOPSIS'])
  z=list(df['VIKOR'])

  result_avg=[]
  for i in range(len(x)):
    x1=x[i]
    y1=y[i]
    z1=z[i]
    r=avg(x1,y1,z1)
    result_avg.append(r)


  df['Average']=result_avg
  df['Average']=result_avg
  print("")
  #predict(out[0],result_avg)

  df.to_csv("output.csv")
  df={"Node":["Node "+str(i+1) for i in range(len(y))],"Results":result_avg}
  maximum=max(result_avg)
  node=result_avg.index(maximum)+1  
  return [df,node,maximum]
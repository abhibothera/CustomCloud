import math
import numpy as np
import pandas as pd
from scipy.stats import rankdata
import argparse

def demo():
    print('TESTING 123')

def tops(datas,impact,c):
    rows= len(datas)
    square = []
    positive =[]
    negative = []

    for i in range(0, len(c)):
        sum=0
        for j in range(0,rows):
            sum = sum + (datas[j,i]*datas[j,i])
        temp= math.sqrt(sum)    
        square.append(temp)
       
    for i in range(0, len(c)):
        for j in range(0,rows):
            datas[j,i]= datas[j,i]+0.0/square[i]+0.0
            datas[j,i]= datas[j,i]*c[i]
        
    for i in range(0, len(c)):
        min = 100000000
        max = -100000000
        for j in range(0,rows):
            if min > datas[j,i]:
                min= datas[j,i]
            if max < datas[j,i]:
                max = datas[j,i]
        if impact[i] == '+':
            positive.append(max)
            negative.append(min)
        if impact[i] == '-':
            positive.append(min)
            negative.append(max)
    
    spositive = []
    snegative = []
    performance = []
    
    for i in range(0,rows):    
        sum=0
        sum1 = 0
        for j in range(0, len(c)):
            sum = sum + (datas[i,j]-positive[j])*(datas[i,j]-positive[j])
            sum1 = sum1 + (datas[i,j]-negative[j])*(datas[i,j]-negative[j])
        sum = math.sqrt(sum)
        sum1 = math.sqrt(sum1)
        spositive.append(sum)
        snegative.append(sum1)
        
    for i in range(0,len(spositive)):
        performance.append(snegative[i]/(spositive[i]+snegative[i]))
    
    datas = np.column_stack((datas,performance))
    #print(datas)
    #last_col = len(datas[0])    
    #datas = datas*-1
    #datas= datas[datas[:,last_col-1].argsort()]
    #datas = datas*-1
    #for i in range(0,rows):
        #datas[i,-1]=i+1
    #temp = datas   
    return datas

def topsi(file,impact,c):
    datas = pd.read_csv(file)
    datas=datas.iloc[:,1:].values
    rows= len(datas)
    square = []
    positive =[]
    negative = []

    for i in range(0, len(c)):
        sum=0
        for j in range(0,rows):
            sum = sum + (datas[j,i]*datas[j,i])
        temp= math.sqrt(sum)    
        square.append(temp)
       
    for i in range(0, len(c)):
        for j in range(0,rows):
            datas[j,i]= datas[j,i]+0.0/square[i]+0.0
            datas[j,i]= datas[j,i]*c[i]
        
    for i in range(0, len(c)):
        min = 100000000
        max = -100000000
        for j in range(0,rows):
            if min > datas[j,i]:
                min= datas[j,i]
            if max < datas[j,i]:
                max = datas[j,i]
        if impact[i] == '+':
            positive.append(max)
            negative.append(min)
        if impact[i] == '-':
            positive.append(min)
            negative.append(max)
    
    spositive = []
    snegative = []
    performance = []
    
    for i in range(0,rows):    
        sum=0
        sum1 = 0
        for j in range(0, len(c)):
            sum = sum + (datas[i,j]-positive[j])*(datas[i,j]-positive[j])
            sum1 = sum1 + (datas[i,j]-negative[j])*(datas[i,j]-negative[j])
        sum = math.sqrt(sum)
        sum1 = math.sqrt(sum1)
        spositive.append(sum)
        snegative.append(sum1)
        
    for i in range(0,len(spositive)):
        performance.append(snegative[i]+0.0/(spositive[i]+0.0+snegative[i]))
        #print(performance)
    
    rank = len(performance) - rankdata(performance, method = 'min').astype(int) + 1
    datas = np.column_stack((datas,rank))
    temp = datas   
    return temp


def main():
 
    ap = argparse.ArgumentParser(description='Calculate Rank with TOPSIS')
    ap.add_argument('-f', '--Filepath', type=str, required=True, default = None, help='filepath of CSV file', dest='filepath')
    ap.add_argument('-z', '--Z', nargs = '+', type=str, required=True, default = None, help="Imapact of each attribute Z('+', '-') of each column", dest='Z')
    ap.add_argument('-w', '--Weights', nargs = '+', type=int, required=True, default = None, help='Weights of each column of the given dataset', dest='W')
    args = ap.parse_args()
    dat = topsi(args.filepath, args.Z, args.W)
    print(dat)
    
if __name__ == '__main__':
    main()

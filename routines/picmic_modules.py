import pandas as pd
import numpy as np
from os import listdir

def check(s, arr):
    result = []
    for i in arr:
        # for every character in char array
        # if it is present in string return true else false
        if i in s:
            result.append("True")
        else:
            result.append("False")
    ##if (len(result)>0) :
    return result[0]


def getPisteId(m_row,m_col):
    
    ##tempdf = pd.read_csv("/home/habreu/WORK/data_bin2ascii/listWays.csv")
    tempdf= pd.read_csv(RC2ALIAS)
    #print("Row-->",m_row,"Col-->",m_col)
    name =  tempdf['Name'][    (tempdf['Column']==m_col) &  (tempdf['Row']==m_row) ].to_list()  
    #print(name)
    #print('len name = ', name)
    #id = tempdf.Name.iloc[name].at(0)
    id = "R"+str(m_row)+"-C"+str(m_col)
    #print("id=",id)
    
    if ( len(name)>0 ) :
        id = name[0].strip()
    del tempdf
    return id

def getPisteIdRaw(m_row,m_col):
    id = "R"+str(m_row)+"-C"+str(m_col)
    return id

def cleanPandaPicmic(mypd, xAxis='VBN_adj') : 
    my_df = mypd.copy()
    my_df = my_df.dropna(axis=1)
    dim_data = len(my_df.columns)
    mylist = []
    mylist.append(xAxis)

    for i in range(1,dim_data) :
        my_pixel = getPisteId(int(my_df.iloc[0].at[i]),int(my_df.iloc[1].at[i]))
        temp = 'VBN_adj' if i == 0 else my_pixel
        mylist.append(temp)

    my_dict = {idx : mylist[idx] for idx in range(0,dim_data)}
    
    my_df.rename(columns = my_dict, inplace=True) # rename columns 0 and 1
    my_df = my_df.tail(-2) # to delete the two first rows
    my_df[xAxis] = my_df[xAxis].astype(int)
    my_df[mylist] = my_df[mylist].astype(float)
    return my_df

def dataframe_concat(var='VRefN',name='concat_scurves.csv'):
    
    mylist = [ x for x in listdir() if x.endswith(".txt") ]    
    dflist = [pd.read_csv(f) for f in mylist]
    
    pd_concat = pd.concat(dflist)
    pd_concat = pd_concat.fillna(0)
    pd_concat = pd_concat.sort_values(by=[var])
   
    pd_concat.reset_index(drop=True, inplace=True)
    pd_concat.sort_index(inplace=True)

    lastIndex = pd_concat.idxmax()[var]
    lastVal = pd_concat[var].min()

    zero = [0 for i in range(len(pd_concat.columns))]
   
    for i in range(lastVal):
        zero[0] = int(i)
        idx=lastIndex+i
        pd_concat.loc[idx] = zero 
  
    pd_concat = pd_concat.sort_values(by='VRefN')
    
    pd_concat.to_csv(name,index=False)
    
    
def dataframe_concat_standalone(mylist, var='VRefN',name='concat_scurves.csv'):
    
    dflist = [pd.read_csv(f) for f in mylist]
    
    pd_concat = pd.concat(dflist)
    pd_concat = pd_concat.fillna(0)
    pd_concat = pd_concat.sort_values(by=[var])
     
    pd_concat.reset_index(drop=True, inplace=True)
    pd_concat.sort_index(inplace=True)
    
    lastIndex = pd_concat.idxmax()[var]
    firstVal = pd_concat[var].min()
    
    zero = [0 for i in range(len(pd_concat.columns))]
    
    
    var_x = pd_concat[var].to_list()
    var_all = np.arange(0,251,1).tolist()
    
    
    for i in var_x:
        var_all.remove(i)
        
    index = len(var_all)
    
    for val in var_all :
        zero[0] = int(val)
        pd_concat.loc[index] = zero
        index+=1 
  
    pd_concat = pd_concat.sort_values(by=[var])
    ##print(pd_concat)
    
    ###exit()
    pd_concat.to_csv(name,index=False)
    
    
def dataframe_concat_standalone_digital(mylist, var='VRefN',name='concat_scurves.csv'):
    
    dflist = [pd.read_csv(f) for f in mylist]
    
    pd_concat = pd.concat(dflist)
    pd_concat = pd_concat.fillna(0)
    pd_concat = pd_concat.sort_values(by=[var])
   
    #print(pd_concat)
   
    pd_concat.reset_index(drop=True, inplace=True)
    pd_concat.sort_index(inplace=True)
    
    lastIndex = pd_concat.idxmax()[var]
    firstVal = pd_concat[var].min()
    #lastVal = pd_concat[var].min()
    
    zero = [0 for i in range(len(pd_concat.columns))]
   
    #print('HERE 01')
   
    #for i in range(lastVal):
    for i in range(0,firstVal):
        zero[0] = int(i)
        idx=lastIndex+i+1
        pd_concat.loc[idx] = zero 
    
    
    #print('HERE 02')
    #pd_concat = pd_concat.sort_values(by='VRefN')
    pd_concat = pd_concat.sort_values(by=[var])
    pd_concat.to_csv(name,index=False)
 
    #print('HERE 03')

#!/usr/bin/env python3
'''
Author :        Edouard BECHETOILE, Henso ABREU
Description:    Script to dump binary data produced by PICMIC0/SAMPIC to an ASCII file 
                "version 4"
'''
import pandas as pd
import numpy as np
import sys
import os
import argparse
import re
import struct
from datetime import date,time
import picmic_modules as prepro
import csv
from termcolor import colored
from collections import OrderedDict
import stat
import shutil

headers = ["nbPixels","timeStamp1","timeStamp2","listPixels"]
##CDW = os.getcwd()   # Actual directory
##print('Directory')
##print(CDW)
##ascii_files = './data_ascii'

##########################################
# function to check string
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

##########################################
def dumpData(list1, list2, list3, list4) :
    myList = []
    myList.append(list1)
    myList.append(list2)
    myList.append(list3)
    myList.append(list4)
    return myList

##########################################
def uncode(f):
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file" , action='store_true',help="provide the binary input file produced by PICMIC0/SAMPIC")
    parser.add_argument("PARAMS", nargs='+')
    parser.add_argument("-o", "--outDir", help="provide the output folder to save the processed ASCII data")
    args, unknown = parser.parse_known_args()
    if not sys.stdin.isatty():
        args.PARAMS.extend(sys.stdin.read().splitlines())
    ''' 
    # loading the tailed file
    ##for f in args.PARAMS :
        ##print(20*'-')
        ##print(f)
        # variable defintions
    dump =1
    nbPixel=0
    mat=[]
    numPixelsList = []
    allPixelsList = []
    timeStampList = []
    timeStampList2 = []
    totalEvts=0
    
    testList = []
    # -----------------------------
    inFileName = ''
    print('INPUT FILE:',f)
    ##if check(f,['/']) :
    if check(f,[os.sep]) :
        ##string_split= f.split('/')
        string_split= f.split(os.sep)
        for s in string_split :
            if not s :
                continue
            ##inFileName+='/'+s
            inFileName+=s+os.sep
            ## inFileName+=s
            if 'run_vrefn' in s:
                break
    else :
        ##inFileName = f.split('/')[0]
        inFileName = f.split(os.sep)[0]
    #------------------------------

    ##print('inFile print:',inFileName)
    ##print(20*'--')
    outFileName = inFileName[:-1].replace(".","_")
    ##print('otufile print:',outFileName)

    if os.path.exists(f):
            ##file = open(f,"rb")
        with open(f,"rb") as file:

            ## Reading information from the file comments
            head=file.readline(); ## line1
            infoFromComments  = str(head).split("==")[2].split("=")[1:]
            runInfo = [i.split(' ')[1] for i in infoFromComments]
    
            head=file.readline(); ## line2
            freq = int(str(head).split("==")[-2].split(' ')[4])

            ## lines 3 
            head=file.readline() # 3 #=== DATA STRUCTURE PER FRAME===
            newVarValues = [int(i.split(' ')[1]) for i in str(head).split(':')[2:] ]
            newVarNames = [ j.split(' ')[-1].strip() for j in str(head).split(':')[1:]]
            dictNewVars = dict(zip(newVarNames,newVarValues))

            head=file.readline() # line 4 # === NB_OF_PIXELS_IN_FRAMES (2 bytes) RAW_TIMESTAMP (in fe_clock_periods) (5 Bytes), PIXEL_COLUMN (1 byte), PIXEL ROW ( 1 byte) ==
            head=file.readline() # line 5 #
            head=file.readline() # line 6 #

            dump_cont = 0 
                
            while dump : 
                    
                dump_cont+=1
                
                dump =int.from_bytes(file.read(2), 'little') 
                timeStamp= file.read(2*4)
                cnt = 0
                ##print("---------------- dump :", dump, " ,  dump cont = ", dump_cont)
                ##if ( dump <= 1 ) :
                ##    break

                while cnt<dump:
                #while :
                    cnt+=1
                    totalEvts+=1
                    nbPixel= int.from_bytes(file.read(2),'little')
                    timeStamp2= file.read(2*4)
                    
                    #print('======== nbPixel:', nbPixel)
                    ##print('======== cnt :', cnt)
                    #print(20*'-')
                    if nbPixel >0:
                        RCs= file.read(2*nbPixel)
                        mat = [[int.from_bytes(RCs[2*i+1:2*i+2],'little'),int.from_bytes(RCs[2*i:2*i+1],'little')] for i in range(nbPixel)] 
                        #print(mat)
                        #print('-----------------------------------------------------------------')
                        ##ch = [ prepro.getPisteId(idx[1],idx[0]) for idx in mat]
                        ch = [ prepro.getPisteIdRaw(idx[1],idx[0]) for idx in mat]
                        
                        #print(ch)
                        #print('-----------------------------------------------------------------')
                        numPixelsList.append(nbPixel)
                
                        timeStampList.append(struct.unpack('<d',timeStamp)[0])
                        timeStampList2.append(struct.unpack('<d',timeStamp2)[0])
                        allPixelsList.append(ch)
                            
                    else:
                        break
                ##break
                ##if ( dump_cont == 1 ) :
                ##    dump = 0

            allData = dumpData(numPixelsList,timeStampList,timeStampList2,allPixelsList)
            myDict = dict(zip(headers,allData))

            df2Csv = pd.DataFrame.from_dict(myDict)
            df2Csv['UnixTime'] = runInfo[0]
            dateformat = runInfo[1].split('.')
            timeformat = runInfo[2].split('.')
            df2Csv['dateTime'] = pd.Timestamp(int(dateformat[0]),int(dateformat[1]),int(dateformat[2]), int(timeformat[0][:-1]), int(timeformat[1][:-1]),  int(timeformat[2][:-1]),int(timeformat[3][:-2]) )
            df2Csv['Freq'] = freq
    
            # loop to add new variable information
            for key, value in dictNewVars.items():
                df2Csv[key] = value

            ##print(outFileName)
            df2Csv.to_csv(outFileName+'.csv', index=False)
    
            file.close()
            print(colored('---- FILE : ' +f+ '  already processed -----','red'))
            print(colored('---- FILE : ' +outFileName+'.csv'+ '  created with List of Pixels and time information -----','blue'))
    
            ##exit()

            ##print('total Events= ', totalEvts)
            ##print('my test --')
            ##print(pd.value_counts(np.hstack(df2Csv.listPixels)).to_dict())

            print(50*'-')
        
            if (df2Csv.empty==False):
            
                ##this_dict = pd.value_counts(np.hstack(df2Csv.listPixels)).to_dict()
                this_dict = pd.Series(np.hstack(df2Csv.listPixels)).value_counts().to_dict()
                ##print(this_dict)
                ##if totalEvts <=1 :
                ##    totalEvts = 1000
                for k, v in this_dict.items() :
                    this_dict[k]= "{0:.3f}".format(v/totalEvts)
                                                     
                ##this_dict.update({'VRefN':"{0:03}".format(df2Csv.VrefN[0])})
                ##this_dict = {'VRefN': this_dict.pop('VRefN'), **this_dict}
                this_dict.update({'VRefP':"{0:03}".format(df2Csv.VrefP[0])})
                ##value_vrefp = this_dict.pop('VRefP',None)
                ##if value_vrefp is not None :
                        
                        ##this_dict = {'VRefP': value_vrefp, **this_dict}
                this_dict = {'VRefP': this_dict.pop('VRefP'), **this_dict}
                
                #this_dict = dict(sorted(this_dict.items(),reverse=True)) 
        
                # sCurve save data
                l1 = ''
                l2 = ''
            
                for idx, k in enumerate(this_dict.keys()) :
                    if (idx != len(this_dict.keys() ) -1) :
                        l1 +=k+','        
                        l2+=str(this_dict[k])+','
                    else :
                        l1+=k+'\n'
                        l2+=str(this_dict[k])+'\n'
                        
        
                l2write = []
                l2write.append(l1)
                l2write.append(l2)
        
                #with open(outFileName+'_VRefN'+str("{0:03}".format(df2Csv.VrefN[0]))+'.txt','w') as w:
                with open(outFileName+'.txt','w') as w:
                    for line in l2write :
                        w.write(line)
        
                print(50*'-')
    else :
            print(f"[WARNING] : {f} does not exist.")
    
## concat Scurve 
#nameScurve = outFileName.replace(outFileName.split('_')[-2],"VRefN-SCAN")
#prepro.dataframe_concat(name=nameScurve+'.csv')
        
####    exit()
##########################################
import os
import shutil
import stat

def remove_with_permissions(path):
    """
    Attempts to delete a file or directory, handling permission errors by
    making files and directories writable and retrying the deletion.
    """
    if os.path.exists(path):
        try:
            # If it's a file, try to delete it directly
            if os.path.isfile(path) or os.path.islink(path):
                os.chmod(path, stat.S_IWRITE)  # Change to writable
                os.remove(path)
                print(f"File deleted: {path}")
            # If it's a directory, delete recursively
            elif os.path.isdir(path):
                shutil.rmtree(path, onerror=handle_permission_error)
                print(f"Directory deleted: {path}")
        except PermissionError as e:
            print(f"Permission error while deleting {path}: {e}")
        except Exception as e:
            print(f"Error while deleting {path}: {e}")
    else:
        print(f"The path '{path}' does not exist or is inaccessible.")

def handle_permission_error(func, path, exc_info):
    """
    Error handler for `shutil.rmtree`.
    Changes the permission of the file/folder to be writable and retries deletion.
    """
    # Change permissions to writable and retry deletion
    try:
        os.chmod(path, stat.S_IWRITE)
        func(path)
    except Exception as e:
        print(f"Failed to delete {path} even after changing permissions. Reason: {e}")

# Usage example
##if __name__ == "__main__":
##    # Define the directory or file you want to delete
##    path_to_delete = r'K:\R'  # Update this with your path

##    # Attempt to delete the specified path
##    remove_with_permissions(path_to_delete)

        

##########################################
def merger(listOfFiles):

    inFileName = listOfFiles[0].split(os.sep)[-1]
    outFileName = inFileName

    folderName = os.path.dirname(listOfFiles[0])
    outFileName = folderName+os.sep+inFileName.split('_')[0]+'_'+inFileName.split('_')[1]

    nameScurve = outFileName+"_VRefP-SCAN"+'.csv'

    prepro.dataframe_concat_standalone(listOfFiles, var='VRefP',name=nameScurve)
    print(' Done : ' +nameScurve+' <<<======'  )

    for filename in os.listdir(folderName):
        if 'VRefP-SCAN' not in filename:
            ####                os.remove(os.path.sep.join([folderName,filename]))
            remove_with_permissions(os.path.sep.join([folderName,filename]))



    

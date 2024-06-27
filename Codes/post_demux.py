#!/usr/bin/env python3
"""
recombines the fast acquisition files from the two PeterBox
"""

import os
import numpy as np

loc1="C:/FTP_root/DATA/acq2106_178/"
loc2="C:/FTP_root/DATA/acq2106_377/"
loc="C:/FTP_root/DATA/"



def select_files_by_type(loc,extension=".npy"):
    """
    Create a list of all the files contained in 'loc' ending in 'extension'
    """
    ls=os.listdir(loc)
    ls_select=[file for file in ls if file[-len(extension):]==extension]
    return(ls_select)

def open_npy_peter(file):
    """
    Open Peter's weird npy files
    """
    loaded = np.load(file,allow_pickle=True)
    dictionnary=loaded.all()
    # Generate the keys (because hell)
    keys=['CH{} V'.format(i) for i in range(1,33)]
    new_array=[]
    for i in range(len(keys)):
        new_array.append(dictionnary[keys[i]])
    new_array=np.array(new_array)
    return(new_array)


ls_select_1=sorted(select_files_by_type(loc1))
ls_select_2=sorted(select_files_by_type(loc2))


for i in range(len(ls_select_1)):
    file1=ls_select_1[i]
    file2=ls_select_2[i]
    arr1=open_npy_peter(loc1+file1)
    arr2=open_npy_peter(loc2+file2)
    arr=np.concatenate((arr1,arr2),0)
    saveloc = loc+file1[:9]+".npy"
    np.save(saveloc,arr)




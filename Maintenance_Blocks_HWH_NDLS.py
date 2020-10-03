#!/usr/bin/env python
# coding: utf-8

# In[13]:


# Maintenance Blocks in HWH-NDLS route 

# First find the direction of the block from station loop and block 
from collections import defaultdict
loop = open('loop.txt').readlines()[2:]
station = open('station.txt').readlines()[2:]
block = open('block.txt').readlines()[2:]

# string = 'CSMT-BY'

loop_dict = {l.split()[0]:l.split()[3] for l in loop}
station_ID = {l.split()[0][0:4]:l.split()[3] for l in loop}
station_ID_reverse = {station_ID[k]:k for k in station_ID}
loop_dir = {l.split()[0]:l.split()[1] for l in loop}
block_dir ={b.split()[0]:b.split()[1] for b in block}
station_dict = defaultdict(list)
# block_links = defaultdict(list)
loop_links = defaultdict(list)
for l in loop:
    station_dict[l.split()[3]].append(l.split()[0])
station_dict = dict(station_dict)


# In[14]:


stn_list = [s.split()[0] for s in station]
def block_direction(string):
    station_1 = string[:string.index('-')]
    station_2 = string[string.index('-')+1:]
    if(stn_list.index(station_1)>stn_list.index(station_2)):
        return 'Down'
    return 'Up'
# print(block_direction('CSMT-BY'))
# print(station_ID_reverse)
# common_lis = ['9117','9118','9119','9120','9142','9143','9144','9145','9146','9147']
common_lis = []
# This common lis has a single line between some stations 


# sp_list = [str(i) for i in range(9187,9205)]                     # Suburban stations CSMT-MAS
sp_list = []
route = 'NDLS-HWH-'
def return_name(sp_list):
    if(len(sp_list)==0):
        return str(route)+'Maintenance-all-3-days.txt'
    else:
        return str(route)+'Maintenance-sub-3-days.txt'
    


def return_block(string):
    if(len(sp_list)!=0):
        if(str(station_ID_reverse[string[:string.index('-')]]) not in sp_list and str(station_ID_reverse[string[string.index('-')+1:]]) not in sp_list):
            return 0
    if(block_direction(string)=='Up'):
        blk = str(station_ID_reverse[string[:string.index('-')]])+'0010'
        if(str(station_ID_reverse[string[:string.index('-')]]) in common_lis):
            blk = str(station_ID_reverse[string[:string.index('-')]])+'2010'    
        return blk
    blk = str(station_ID_reverse[string[string.index('-')+1:]])+'1010'
    if(str(station_ID_reverse[string[string.index('-')+1:]]) in common_lis):
        blk = str(station_ID_reverse[string[string.index('-')+1:]])+'2010'
    return blk


# In[15]:


# Also incorporate a facility to put suburban maintenance blocks 

import pandas as pd
df = pd.read_excel('Maintenance_Sheet.xlsx')
df.drop_duplicates(subset=['Section','Start','End'], keep=False,inplace=True)
print(df)
# Directly reading from the Sheet 
with open(return_name(sp_list),'w') as mf:
    mf.write('/*Comment*/')
    mf.write('\n\n')
    for index,k in df.iterrows():
        
        try:
            if(not return_block(k['Section'])):
                continue
            mf.write(str(return_block(k['Section'])))
            mf.write(' ')
            mf.write('"'+str(int(float(k['Start'])/60))+'"')
            mf.write(' ')
            mf.write('"'+str(int(float(k['End'])/60))+'"')
            mf.write(' ')
            mf.write('"none"')
            mf.write('\n')
            mf.write(str(return_block(k['Section'])))
            mf.write(' ')
            mf.write('"'+str(int(float(k['Start'])/60+1440))+'"')
            mf.write(' ')
            mf.write('"'+str(int(float(k['End'])/60+1440))+'"')
            mf.write(' ')
            mf.write('"none"')
            mf.write('\n')
            mf.write(str(return_block(k['Section'])))
            mf.write(' ')
            mf.write('"'+str(int(float(k['Start'])/60+2880))+'"')
            mf.write(' ')
            mf.write('"'+str(int(float(k['End'])/60+2880))+'"')
            mf.write(' ')
            mf.write('"none"')
            mf.write('\n')
        except:
            print(k['Section'])
mf.close()


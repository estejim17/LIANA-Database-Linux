#importacion de selenium y modulos relacionados
import time
import datetime
#from bs4 import BeautifulSoup
import requests
import progressbar
import string

import numpy as np
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
import os
import sys


def dataRead():
    df = pd.read_excel('../database/output.xlsx', sheet_name='hsa-let-7a-5p')
    df1 = pd.read_excel('../database/Datos1.xlsx')
    if df1.empty:
        inicio = 0
        lista2 = []
    else:
        lista2 = df1.values[:,1].tolist()
        inicio = len(lista2)
        
    listRNA = df.values[:,1]    
    return listRNA, lista2, inicio

listRNA, lista2, inicio = dataRead()
cadenas = lista2
# print(listRNA)

df1 = pd.read_excel('../database/Datos1.xlsx')


disease_list_url = "http://bioinfo.life.hust.edu.cn/lncRNASNP/api/exp_disease_list?index={}&page={}"

incRNA = []
diseases = []
pubMed = []
chrom = []
print()
# sys.stdout.write("Obteniendo información de sitio web...")
print('Obteniendo información de sitio web...')


indexes = {'A':2, 'B':4, 'C':4, 'D':1, 'E':1, 'F':1, 
        'G':2, 'H':2, 'I':1, 'K':1, 'L':2, 'M':2, 
        'N':1, 'O':1, 'P':3, 'R':1, 'S':2, 'T':2, 
        'U':1, 'V':1, 'W':1}

bar = progressbar.ProgressBar(maxval=36, \
    widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
bar.start()
count = 0
for key in (indexes.keys()):
    for i in range(1,indexes[key]+1):
        response = requests.get(disease_list_url.format(key, i)).json()
        df = pd.DataFrame(response["lncrna_gene_list"])
        # print(df)
        incRNA.extend(df['lncrna'].tolist())
        diseases.extend(df['disease'].tolist())
        chrom.extend(df['chromosome'].tolist())
        pubMed.extend(df['pubmed'].tolist())
        # print(incRNA)
        # print(diseases)
        # print(chrom)
        # print(pubMed)
        count = count + 1
        bar.update(count)
bar.finish()
print('              ---------------------LISTO---------------------')
indices = []
indices2 = []

excel1 = ['-']*len(listRNA)
excel2 = ['-']*len(listRNA)
excel3 = ['-']*len(listRNA)
excel4 = ['-']*len(listRNA)

for j in range(len(listRNA)):
    for i in range(len(incRNA)):
        if incRNA[i] == listRNA[j]:
            excel1[j] = incRNA[i]
            excel2[j] = diseases[i]
            excel3[j] = chrom[i]
            excel4[j] = pubMed[i]
            indices.append(j)
            indices2.append(i)

df = pd.DataFrame.from_dict({'incRNA':excel1,'Diseases':excel2, 'Chromosome':excel3, 'pubMed':excel4})
df.to_excel('../database/Diseases.xlsx', header=True, index=False)



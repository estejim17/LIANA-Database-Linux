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
from openpyxl import load_workbook

import ExtractmirRNA
import atexit

def exit_handler():
    output['cancer related'] = disCol
    output.to_excel(writer, sheet)
    writer.save()
atexit.register(exit_handler)

listmiRNA = ExtractmirRNA.getmiRNA()

def dataRead(sheet1):
    #se leen los archivos excel para extraer los datos necesarios.
    output = pd.read_excel('/home/estejim15/LIANA-Database-Linux/database/output.xlsx', sheet1, engine='openpyxl')   

    listINC = output['lncRNA'].tolist()
    return output, listINC




# print(listRNA)



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
        for idx, value in enumerate(df['disease'].tolist()):
            disease = value.lower()
            if 'leukemia' in disease or 'cancer' in disease or 'carcinoma' in disease or 'lymphoma' in disease or 'melanoma' in disease or 'medulloblastoma' in disease or 'neuroblastoma' in disease or 'osteosarcoma' in disease or 'rhabdomyosarcoma' in disease or 'tumor' in disease or 'meningioma' in disease :
                incRNA.append(df['lncrna'].tolist()[idx])
                diseases.append(disease)
        # print(df)
        # incRNA.extend(df['lncrna'].tolist())
        # diseases.extend(df['disease'].tolist())
        # chrom.extend(df['chromosome'].tolist())
        # pubMed.extend(df['pubmed'].tolist())
        # print(incRNA)
        # print(diseases)
        # print(chrom)
        # print(pubMed)
        count = count + 1
        bar.update(count)
bar.finish()
print('              ---------------------LISTO---------------------')


counter = 1
for sheet in listmiRNA:

    
    print(str(counter) + "- "+ sheet)  
    counter += 1
    output, listINC = dataRead(sheet)

    wb = load_workbook('/home/estejim15/LIANA-Database-Linux/database/output.xlsx') 
    wb.remove(wb[sheet])
    wb.save('/home/estejim15/LIANA-Database-Linux/database/output.xlsx')

    disCol = [0]*len(listINC)
    writer = pd.ExcelWriter('/home/estejim15/LIANA-Database-Linux/database/output.xlsx', mode='a', engine='openpyxl')
    for i in range(len(listINC)):
        print('Comparando incRNA {}'.format(i))
        for j in range(len(incRNA)):
            if j == i:
                disCol[i] = 1
        
    output['cancer related'] = disCol
    output.to_excel(writer, sheet)
    writer.save()
print(incRNA)
print(diseases)
# indices = []
# indices2 = []

# excel1 = ['-']*len(listRNA)
# excel2 = ['-']*len(listRNA)
# excel3 = ['-']*len(listRNA)
# excel4 = ['-']*len(listRNA)

# for j in range(len(listRNA)):
#     for i in range(len(incRNA)):
#         if incRNA[i] == listRNA[j]:
#             excel1[j] = incRNA[i]
#             excel2[j] = diseases[i]
#             # excel3[j] = chrom[i]
#             # excel4[j] = pubMed[i]
#             indices.append(j)
#             indices2.append(i)

# df = pd.DataFrame.from_dict({'incRNA':excel1,'Diseases':excel2})
# df.to_excel('../database/Diseases.xlsx', header=True, index=False)



#!/usr/bin/python
# coding=utf-8

#importacion de selenium y modulos relacionados
import time
import datetime
import requests 
import string

import numpy as np
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
import os
import sys
import xlrd

import ExtractmirRNA

from openpyxl import load_workbook


import atexit

def exit_handler():
    writer.save()
atexit.register(exit_handler)


listmiRNA = ExtractmirRNA.getmiRNA()


def dataRead(sheet1):
    data = pd.read_excel('./database/Datos1.xlsx', None)

    #en caso que el archivo este abierto
    exception = True
    while exception:
        try:
            df = pd.read_excel('./database/output.xlsx', sheet1)
            exception = False
        except:
            exception = True
            print('Archivo output.xlsx en uso... Intentando de nuevo.')
            time.sleep(5)

    if not sheet1 in data.keys(): 
        inicio = 0
        lista2 = []
    else:        
        df1 = pd.read_excel('./database/Datos1.xlsx', sheet1)
        if df1.empty:
            inicio = 0
            lista2 = []
        else:
            lista2 = df1.values[:,1].tolist()
            inicio = len(lista2)

    listRNA = df.values[:,1]    
    return listRNA, lista2, inicio

link = "http://bioinfo.life.hust.edu.cn/static/lncRNASNP2/download_sequence/lncrna/{}"



for j in listmiRNA:
    listRNA, lista2, inicio = dataRead(j)
    
    cadenas = lista2
    print(j)  

    if inicio != len(listRNA): 
    
    
        if inicio < len(listRNA) and inicio > 0:
            wb = load_workbook('./database/Datos1.xlsx') 
            wb.remove(wb[j])
            wb.save('./database/Datos1.xlsx')
        

        options = {}
        options['strings_to_formulas'] = False
        options['strings_to_urls'] = False
        #pylint: disable=abstract-class-instantiated
        writer = pd.ExcelWriter('./database/Datos1.xlsx', mode='a', engine='openpyxl',options=options)
        for i in range(inicio, len(listRNA)):        
            
            r = ''
            while r == '':
                try:
                    r = requests.get(link.format(listRNA[i]))
                    break
                except:
                    print("Connection refused by the server..")
                    time.sleep(5)
            
            chain = r.text

            if 'Not Found' in chain or chain == '':
                cadenas.append('ERROR')
                print('El gen {} no se encuentra en la página'.format(listRNA[i]))
            else:
                finalChain = chain.splitlines()[1]
                print('Copiando secuencia {}'.format(i))
                cadenas.append((finalChain))
            df1= pd.Series(cadenas)
            df1.to_excel(writer, j)

        writer.save()
        
        

print(cadenas)







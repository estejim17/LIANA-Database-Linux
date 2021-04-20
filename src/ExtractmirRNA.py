#importacion de selenium y modulos relacionados

import requests
import progressbar
import string

import numpy as np
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
import os
import sys
import time

#links para extraer los datos

urlmiRNAnames = "http://bioinfo.life.hust.edu.cn/lncRNASNP/api/mir_expression_list"
url = "http://bioinfo.life.hust.edu.cn/lncRNASNP/api/mirna_target_list?mirna={}"


#esta funcion extrae todas las opciones de miRNA de expresion alta
def getmiRNA():
    response = ''
    while response == '':
        try:
            response = requests.get(urlmiRNAnames).json()
            break
        except:
            print("Connection refused by the server..")
            print("Let me sleep for 5 seconds")
            print("ZZzzzz...")
            time.sleep(5)
            print("Was a nice sleep, now let me continue...")
            continue
    df = pd.DataFrame(response["hmirna_list"])
    listmiRNA = df["miRNA"].tolist()
    return listmiRNA

#se crea lista (se elimina el primer elemento porque ese ya se habia realizado previamente)

def fillDB():
    listmiRNA = getmiRNA()


    writer = pd.ExcelWriter('./database/output.xlsx')

    #barra paraa supervisar proceso
    bar = progressbar.ProgressBar(maxval=len(listmiRNA), \
        widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
    bar.start()
    count = 0

    #recorre la lista con cada miRNA, crea la base de datos utilizando el segundo url,
    #el cual contiene todas las tablas provenientes de la API del sitio web

    for i in listmiRNA:
        response = requests.get(url.format(i)).json()

        conserved = pd.DataFrame(response["cons_target_ls"])
        conserved = conserved[['lncRNA','query','ref','chromosome',"m_start", "m_end","energy","score","conserve"]] #reorganiza y elimina las columnas innecesarias
        conserved['query'] = conserved['query'].map(lambda x: x.lstrip("miRNA: 3' ").rstrip("5'"))
        conserved['ref'] = conserved['ref'].map(lambda x: x.lstrip("lncRNA:5' ").rstrip("3'"))

        nonconserved = pd.DataFrame(response["non_cons_target_ls"])
        nonconserved = nonconserved[['lncRNA','query','ref','chromosome',"m_start", "m_end","energy","score","conserve"]]
        nonconserved['query'] = nonconserved['query'].map(lambda x: x.lstrip("miRNA: 3' ").rstrip("5'"))
        nonconserved['ref'] = nonconserved['ref'].map(lambda x: x.lstrip("lncRNA:5' ").rstrip("3'"))

        df = conserved.append(nonconserved)

        #agrega columnas vacias que se completan posteriormente (con Auto-Chains.py y LinearFold.py)
        df["Cadena"] = ''
        df["CONTRA-FOLD"] = ''
        df["C-Energía"] = ''
        df["VIENNA"] = ''
        df["V-Energía"] = ''

        #reorganiza las columnas en el orden adecuado
        df = df[['lncRNA', 'Cadena', 'CONTRA-FOLD','C-Energía','VIENNA','V-Energía', 'query','ref','chromosome',"m_start", "m_end","energy","score","conserve"]]

        df.to_excel(writer, i)
        count = count + 1
        bar.update(count)

    bar.finish() 
    writer.save() #guarda el archivo excel, cada miRNA se guarda en una hoja de excel distinta




#importacion de selenium y modulos relacionados
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

import requests
import progressbar
import string
import datetime

import numpy as np
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
import os
import sys
#!/usr/bin/python
# coding=utf-8
import time
from openpyxl import load_workbook

import ExtractmirRNA
import CheckVersion

import atexit

def exit_handler():
    df1 = pd.DataFrame()
    df2 = pd.DataFrame()
    df3 = pd.DataFrame()
    df1['lncRNA'] = output['lncRNA']
    df1['Cadenas'] = cadenas
    df2['CONTRA-FOLD'] = linearfoldC
    df2['C-Enegía'] = energia
    df2['VIENNA'] = linearfoldV
    df2['V-Energía'] = energiaV
    df3['query'] = output['query']
    df3['ref'] = output['ref']
    df3['chromosome'] = output['chromosome']
    df3['m_start'] = output['m_start']
    df3['m_end'] = output['m_end']
    df3['energy'] = output['energy']
    df3['score'] = output['score']
    df3['conserve'] = output['conserve']*1
    df1 = pd.concat([df1,df2,df3], ignore_index=True, axis=1)
    df1.columns = ['lncRNA','Cadena','CONTRA-FOLD','C-Energía','VIENNA','V-Energía',
                'query','ref','chromosome','m_start','m_end','energy','score','conserve']        
    df1.to_csv(writer, j)
    writer.save()
atexit.register(exit_handler)

#se checkea la version de chrome y si es necesario descarga el driver para selenium

#se extraen miRNA usando la funcion de ExtractmirRNA.py
listmiRNA = ExtractmirRNA.getmiRNA()


def dataRead(sheet1):
    #se leen los archivos excel para extraer los datos necesarios.
    #se necesitan: las cadenas para buscar en linearfold, los demas datos ya extraidos
    #de linearfold para continuar con la extraccion
    output = pd.read_csv('/home/estejim15/LIANA-Database-Linux/database/output.csv', sheet1)
    df1 = pd.read_csv('/home/estejim15/LIANA-Database-Linux/database/Datos1.csv', sheet1)
    cadenas = df1.values[:,1].tolist()
    if len(output['CONTRA-FOLD'].dropna()) == 0:
        inicio = 0
        linearfoldC = []
        energia = []
        linearfoldV = []
        energiaV = []
    else:
        linearfoldC = output['CONTRA-FOLD'].dropna().tolist()
        energia = output['C-Energía'].dropna().tolist()
        linearfoldV = output['VIENNA'].dropna().tolist()
        energiaV =  output['V-Energía'].dropna().tolist()
        inicio = len(linearfoldC)
    

    listRNA = output['lncRNA'].tolist()
    return output, listRNA, cadenas, inicio, linearfoldC, energia, linearfoldV, linearfoldV, energiaV

linkAPI = "http://linearfold.org/pairingRes/{}"
linkSel = 'http://linearfold.org/'


#se crea instancia de selenium

driver = webdriver.Chrome()
action = ActionChains(driver)

def APIaccess(linkAPI, idCadena):
    #funcion para acceder a la api de linearfold.org, se descarga el archivo y se 
    #lee en formato JSON para extraer la info necesaria
    r = ''
    while r == '':
        try:
            r = requests.get(linkAPI.format(idCadena))
            break
        except:
            print("Connection refused by the server..")
            time.sleep(5)
    r = r.json()
    return r
    

for j in listmiRNA:
    #se recorren todos los miRNA (cada worksheet de excel es uno)
    output, listRNA, cadenas, inicio, linearfoldC, energia, linearfoldV, linearfoldV, energiaV = dataRead(j)
    

    print(j)  



    if inicio != len(cadenas): 
        #para evitar que se lean todos los excel aunque ya hayan
        #sido completados
    
        #se borran los worksheets en los que se esta trabajando
        #para luego crear un duplicado y evitar que hayan dos iguales
        wb = load_workbook('/home/estejim15/LIANA-Database-Linux/database/output.csv') 
        wb.remove(wb[j])
        wb.save('/home/estejim15/LIANA-Database-Linux/database/output.csv')
    
        #se crea instancia de ExcelWriter para leer el excel 
        options = {}
        options['strings_to_formulas'] = False
        options['strings_to_urls'] = False
        #pylint: disable=abstract-class-instantiated
        writer = pd.ExcelWriter('/home/estejim15/LIANA-Database-Linux/database/output.csv', mode='a', engine='openpyxl')
        for i in range(inicio, len(cadenas)): 

            #se accede al sitio web con selenium y se sigue el workflow necesario
            #en la pagina
            driver.get(linkSel)
            while(len(driver.find_elements_by_id("path"))<=0 ):   
                driver.get(linkSel)        
                try:            
                    element = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.ID,'seqInput' ))
                    )
                    driver.find_element_by_id("seqInput").send_keys(Keys.CONTROL, 'a')
                    driver.find_element_by_id("seqInput").send_keys(cadenas[i])
                    time.sleep(2)
                    driver.find_element_by_xpath("/html/body/fieldset[1]/form/input[1]").click()
                    
                except:
                    fecha = str(datetime.datetime.now())
                    print("Page refreshed at time: " + fecha + " because it didn't load properly")
                    time.sleep(1)
           
            try:
            
                    element = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.ID,'path' ))
                    )
                    idCadena = driver.find_element_by_id("path").get_attribute('innerHTML')
                    
                    r = APIaccess(linkAPI, idCadena)
                    
                    linearfoldC.append(r['pairing'][6])
                    energia.append(float(r['pairing'][8][2]))
                    linearfoldV.append(r['pairing'][7])
                    energiaV.append(float(r['pairing'][12][2]))
                    print('Copiando secuencia {}'.format(i))
                    
            except:
                print('Fallo en cargar datos.')
                linearfoldC.append('Error')
                energia.append('Error')
                linearfoldV.append('Error')
                energiaV.append('Error')

        #se crean distintos dataframes para unir todos los datos al final de la extraccion
        #luego se escriben en el excel y se guarda
        df1 = pd.DataFrame()
        df2 = pd.DataFrame()
        df3 = pd.DataFrame()
        df1['lncRNA'] = output['lncRNA']
        df1['Cadenas'] = cadenas
        df2['CONTRA-FOLD'] = linearfoldC
        df2['C-Enegía'] = energia
        df2['VIENNA'] = linearfoldV
        df2['V-Energía'] = energiaV
        df3['query'] = output['query']
        df3['ref'] = output['ref']
        df3['chromosome'] = output['chromosome']
        df3['m_start'] = output['m_start']
        df3['m_end'] = output['m_end']
        df3['energy'] = output['energy']
        df3['score'] = output['score']
        df3['conserve'] = output['conserve']*1
        df1 = pd.concat([df1,df2,df3], ignore_index=True, axis=1)
        df1.columns = ['lncRNA','Cadena','CONTRA-FOLD','C-Energía','VIENNA','V-Energía',
                        'query','ref','chromosome','m_start','m_end','energy','score','conserve']
        df1.to_csv(writer, j)
        writer.save()

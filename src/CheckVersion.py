#!/usr/bin/python
# coding=utf-8

#importacion de selenium y modulos relacionados
from selenium import webdriver

import requests

import os
import sys
import wget
import zipfile




def checkChromeVersion():

    print('Checkeando version de Chrome actual...')

    url = 'https://chromedriver.storage.googleapis.com/LATEST_RELEASE_{}'
    
    



    ## Se debe encontrar la version actual de chrome
    

    driver = webdriver.Chrome()
    driver.minimize_window()
    versionBrowser = driver.capabilities['browserVersion']
    versionDriver = driver.capabilities['chrome']['chromedriverVersion'].split(' ')[0]
    response = requests.get(url.format(versionBrowser[0:2]))
    version_new = response.text

    
    if versionDriver[0:2] != versionBrowser[0:2]:  #en caso de que haya una version más nueva
        respuesta = str(input('Se debe instalar una version nueva del chromedriver, desea instalarla ya? y/n: '))
        if respuesta == 'y':
            # build the donwload url
            download_url = "https://chromedriver.storage.googleapis.com/" + version_new +"/chromedriver_win32.zip"
            # download the zip file using the url built above
            latest_driver_zip = wget.download(download_url,'chromedriver\\chromedriver.zip')
            # extract the zip file
            with zipfile.ZipFile(latest_driver_zip, 'r') as zip_ref:
                zip_ref.extractall('chromedriver\\') 
            # delete the zip file downloaded above
            os.remove(latest_driver_zip)
    driver.quit()


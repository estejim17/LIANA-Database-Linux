# LIANA-Database-Linux
Utilizado para automatizar el proceso de recolección de datos para el proyecto del LIANA que involucra compensación genética en cáncer aneuploide.

Para utilizarlo:

Bibliotecas necesarias:

1. Pandas 
2. Selenium 
3. Requests 
4. Openpyxl
5. Datetime 
6. Progressbar
7. Wget
8. Numpy

Para instalar las bibliotecas:

**Opción 1:**
Instalar bibliotecas necesarias por medio del comando:


```python
pip install -r requirements.txt
```

**Opción 2:**
Abrir CMD o cualquier terminal y escribir "pip install xxxxxx" para cada biblioteca necesaria.

Ejemplo: 
```python
pip install selenium
```

NOTA: Selenium necesita un chromedriver. Para instalar en Linux:

1. Primero es necesario instalar Google Chrome:

```
sudo apt-get install libxss1 libappindicator1 libindicator7
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb

sudo dpkg -i google-chrome*.deb
sudo apt-get install -f

```

2. Luego, se instala el Chromedriver (**NOTA: en el link del codigo siguiente, reemplazar el XX.X.XXXX.XX por la versión del chromedriver correspondiente a la versión actual de Google Chrome. Esto se puede ver aqui:** https://chromedriver.chromium.org/home):

```
sudo apt-get install unzip

wget -N https://chromedriver.storage.googleapis.com/XX.X.XXXX.XX/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
chmod +x chromedriver

sudo mv -f chromedriver /usr/local/share/chromedriver
sudo ln -s /usr/local/share/chromedriver /usr/local/bin/chromedriver
sudo ln -s /usr/local/share/chromedriver /usr/bin/chromedriver

```


>Obtenido de: https://christopher.su/2015/selenium-chromedriver-ubuntu/
---------------------------------------------------------------------------------------------------------------------------

ACTUALIZACIÓN 4/10/2021:

NONCODE.org ha dejado de funcionar. El archivo Auto-Chains.py extrae los datos directamente de la API de bioinfo.life. 
En caso de que NONCODE.org vuelva a funcionar, se puede usar Auto-Chains-Backup.py

# LIANA-Database
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

Abrir CMD o cualquier terminal y escribir "pip install xxxxxx" 

Ejemplo: 
```python
pip install selenium
```

NOTA: Selenium necesita un chromedriver. Este ya viene instalado en el repertorio. Si se tiene una versión distinta, al ejecutar LinearFold.py se notificará y preguntará si se desea hacer la actualización.

---------------------------------------------------------------------------------------------------------------------------

ACTUALIZACIÓN 4/10/2021:

NONCODE.org ha dejado de funcionar. El archivo Auto-Chains.py extrae los datos directamente de la API de bioinfo.life. 
En caso de que NONCODE.org vuelva a funcionar, se puede usar Auto-Chains-Backup.py

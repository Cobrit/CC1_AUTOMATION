import os
import pandas as pd
from selenium import webdriver
from seleniumbase import Driver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import numpy as np
import click
import os


@click.command()
@click.option('--cartera', prompt = 'Ingresa la cartera', help = "La cartera a descargar sus audios")

def rename_downloaded_file(id_value):
    # Especifica la ruta completa donde deseas guardar los archivos
    save_directory = r'C:\Users\DELL PREMIUM\Documents\REPOSITORIOS\CC1_AUTOMATION\DESCARGA'
    # Supongamos que el archivo se descargó en el directorio actual
    download_directory = os.getcwd()

    # Encuentra el archivo descargado (puedes ajustar el patrón según la descarga)
    for filename in os.listdir(download_directory):
        if filename.startswith(f"{id_value}_") and filename.endswith(file_extension):
            # Construye la ruta completa del nuevo archivo con el ID
            new_filepath = os.path.join(save_directory, filename)

            # Construye la ruta completa del archivo descargado actual
            current_filepath = os.path.join(download_directory, filename)

            # Mueve el archivo a la ubicación deseada y renómbralo
            os.rename(current_filepath, new_filepath)


@click.command()
@click.option('--cartera', prompt = 'Ingresa la cartera', help = "La cartera a descargar sus audios")
def cc1_automation(cartera):
    url = "https://app.ccc.uno/Campaign"

    # Configuración para evitar notificaciones
    chrome_options = Options()
    chrome_options.add_experimental_option("prefs", {
        "profile.default_content_setting_values.notifications": 1,
        "download.prompt_for_download": False,  # Desactiva la ventana emergente de descarga
    "download.directory_upgrade": True,
    "safebrowsing.enabled": False,  # Desactiva la verificación de seguridad de descargas
    "plugins.always_open_pdf_externally": True,
})
    # Configuración para ingresar al explorador
    driver = webdriver.Chrome(options = chrome_options)
    driver.get(url)
    wait = WebDriverWait(driver, 10)

    user = "IA"
    user_entry = driver.find_element(By.ID, "username")
    user_entry.send_keys(user)
    password = "25i6%8c4F@"
    password_entry = driver.find_element(By.ID, "password")
    password_entry.send_keys(password)
    login = driver.find_element(By.ID, "btnSave")
    login.click()
    #time.sleep(10)
    driver.switch_to.frame(1)
    
    list_cartera = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'select2-selection__rendered')))
    list_cartera.click()
    search_input = wait.until(
    EC.presence_of_element_located((By.CLASS_NAME, "select2-search__field"))
)
    
    search_input.send_keys(cartera)
    driver.switch_to.active_element.send_keys(Keys.ENTER)

    historial = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="side-nav"]/li[6]')))
    historial.click()
    time.sleep(5)
    grabaciones = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="QFiltersCallStatus-CallRecord"]/label[4]/span')))
    grabaciones.click()
    time.sleep(5) 
    df = []

   # Inicializar una variable para contar las páginas
    page_number = 1

    # Buscar el botón de "Siguiente" por título y clase
    next_button = driver.find_element(By.XPATH, '//a[@title="Siguiente"]/i[@class="fa fa-angle-right fa-lg"]')

    while True:
        table = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'table-responsive')))
        label = wait.until(EC.presence_of_element_located((By.TAG_NAME, 'thead')))
        
        # Obtener las filas después de hacer clic en "Siguiente"
        rows = driver.find_elements(By.TAG_NAME, 'tr')  
        labels = []
        for row in rows:

            # Obtén el ID de la grabación, supongamos que está en la primera columna (cambia el índice si es diferente)
            id_column = row.find_element(By.TAG_NAME, 'td')[0]
            id_value = id_column.text
            print(id_value)

            buttons = row.find_elements(By.TAG_NAME, 'button')
            for button in buttons:
                onclick = button.get_attribute('onclick')
                if onclick and 'DownloadCallRecording' in onclick:
                    driver.execute_script("arguments[0].scrollIntoView();", button)
                    time.sleep(2)
                    button.click()

                    #Renombra el archivo de descarga
                    rename_downloaded_file(id_value)
            encabezado = driver.find_elements(By.TAG_NAME, 'th')
            labels.append(row.text)
            datos = driver.find_elements(By.TAG_NAME, 'td')
            df.append(row.text)



        # Verificar si el botón está deshabilitado
        is_disabled = "disabled" in next_button.find_element(By.XPATH, ('../..')).get_attribute("class")
        if is_disabled:
            print("Botón 'Siguiente' deshabilitado. Has llegado al final de las páginas.")
            break
        
        next_button.click()
        time.sleep(5)
        # Actualizar el botón "Siguiente" para la próxima iteración
        next_button = driver.find_element(By.XPATH, '//a[@title="Siguiente"]/i[@class="fa fa-angle-right fa-lg"]')
        
        # Incrementar el número de página
        page_number += 1

    # Cierra el navegador
    driver.quit()
    print(df) 

if __name__ == '__main__':
    cc1_automation()

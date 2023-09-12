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

    #html = driver.page_source
    #print(html)
    historial = driver.find_element(By.XPATH, '//*[@id="side-nav"]/li[6]')
    historial.click()
    time.sleep(5)
    grabaciones = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="QFiltersCallStatus-CallRecord"]/label[4]/span')))
    grabaciones.click()
    time.sleep(5)
    
    time.sleep(2)
    #final = driver.find_element(By.XPATH, '//*[@id="divBackgrid-CallRecord"]/div/ul/li[14]/a/i')
    #driver.execute_script("arguments[0].scrollIntoView();", final)
    #final.click()
    #time.sleep(5)
    # Encuentra todos los elementos "a" que contienen números de página en el título
    #page_elements = driver.find_elements(By.XPATH, '//a[starts-with(@title, "Page ")]')
    # Inicializa una lista para almacenar los números de página como enteros
    #page_numbers = []

    

    # Extrae los números de página y los convierte en enteros
    #for page_element in page_elements:
     #   page_title = page_element.get_attribute("title")
      #  page_number = int(page_title.split(" ")[1])  # Divide el título y toma el número
       # page_numbers.append(page_number)

    # Obtiene el número máximo de página
    #max_page_number = max(page_numbers)
    #inicio = driver.find_element(By.XPATH, '//*[@id="divBackgrid-CallRecord"]/div/ul/li[1]/a/i')
    #inicio.click()
    
    df = []

    #for page_number in range(1, max_page_number + 1):
    

    # Encontrar el botón de "Siguiente"
    next_button = driver.find_element(By.CSS_SELECTOR, 'a i.fa.fa-angle-right.fa-lg')
    # Inicializar una variable para contar las páginas
    page_number = 1
    while "disabled" not in next_button.get_attribute("class"):
        table = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'table-responsive')))
        label = wait.until(EC.presence_of_element_located((By.TAG_NAME, 'thead')))
        
        # Obtener las filas después de hacer clic en "Siguiente"
        rows = driver.find_elements(By.TAG_NAME, 'tr')  
        labels = []
        for row in rows:
            buttons = row.find_elements(By.TAG_NAME, 'button')
            for button in buttons:
                onclick = button.get_attribute('onclick')
                if onclick and 'DownloadCallRecording' in onclick:
                    driver.execute_script("arguments[0].scrollIntoView();", button)
                    time.sleep(2)
                    button.click()
                    # Realiza aquí la lógica para descargar el archivo

            encabezado = driver.find_elements(By.TAG_NAME, 'th')
            labels.append(row.text)
            datos = driver.find_elements(By.TAG_NAME, 'td')
            df.append(row.text)
    
        next_button.click()
        time.sleep(5)
        # Actualizar el botón "Siguiente" para la próxima iteración
        next_button = driver.find_element(By.CSS_SELECTOR, 'a i.fa.fa-angle-right.fa-lg')
        
        # Incrementar el número de página
        page_number += 1

    # Cierra el navegador
    driver.quit()
    print(df) 

if __name__ == '__main__':
    cc1_automation()

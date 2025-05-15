from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from dotenv import load_dotenv
from selenium.common.exceptions import TimeoutException
import time
import pandas as pd 
import os
import traceback

def login(driver, username, password):
    driver.get('https://visiong.iagree.co/iAgree/faces/gui/campana/arte/ARTE.xhtml')
    driver.maximize_window()
    time.sleep(4)
    assert "i Agree 2.0" in driver.title
    user = driver.find_element(By.NAME, "loginForm:j_idt22")
    user.send_keys(username)

    password_field = driver.find_element(By.NAME, "loginForm:j_idt24")
    password_field.send_keys(password)

    captcha_text = driver.find_element(By.ID, "captcha") 
    captcha_input = driver.find_element(By.NAME, "loginForm:j_idt26")
    captcha_input.send_keys(captcha_text.text)
    captcha_input.send_keys(Keys.RETURN)

def select_campaign(driver):
    time.sleep(5)
    ingresar_leonisa_link = driver.find_element(By.XPATH, "//*[@id='mainForm:j_idt106:0:j_idt112']/span")
    ingresar_leonisa_link.click()
    time.sleep(3)

def client_management(driver, cedula, telefono_csv):
    time.sleep(5)

    cedula_input = driver.find_element(By.XPATH, "//*[@id='topBarForm:itBuscarGenerico']")
    acciones = ActionChains(driver)
    acciones.double_click(cedula_input).perform()
    time.sleep(2)
    cedula_input.send_keys(cedula)
    time.sleep(3)
    cedula_input.send_keys(Keys.ENTER)
    time.sleep(3)

    try:
        driver.find_element(By.XPATH, "//*[@id='mainForm:idDtDeudoresObligaciones_data']/tr/td[3]").click()
        time.sleep(3)
    except Exception:
        driver.find_element(By.XPATH, "//*[@id='mainForm:dtDeudoresBusqueda_data']/tr/td[5]").click()
        time.sleep(3)
        driver.find_element(By.XPATH, "//*[@id='mainForm:j_idt2498']/span").click()
        time.sleep(4)

    # Seleccionar telefono segun el CSV
    wait = WebDriverWait(driver, 10)
    telefonos_fila = wait.until(
        EC.presence_of_all_elements_located((By.XPATH, "//*[@id='mainForm:pgRenderisarDatosContacto:dtTelefonosDeudorData_data']/tr"))
    )

    telefono_encontrado = False
    for fila in telefonos_fila:
        try:
            numero_element = fila.find_element(By.XPATH, "./td[2]")
            numero_texto = numero_element.text.strip().replace(" ", "")
            if telefono_csv in numero_texto:
                numero_element.click()
                telefono_encontrado = True
                time.sleep(2)
                break
        except Exception:
            continue

    if not telefono_encontrado:
        raise Exception(f"TelÃ©fono {telefono_csv} no encontrado en la tabla")

    driver.find_element(By.XPATH, "//*[@id='mainForm:dtAgreeGuiones_data']/tr[11]/td/span").click()
    time.sleep(4)

    try:
        wait = WebDriverWait(driver, 5)
        keep_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'MANTENER')]")))
        keep_button.click()
        time.sleep(4)
    except TimeoutException:
        wait = WebDriverWait(driver, 4)
        causales_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='mainForm:j_idt1748_data']/tr/td")))
        causales_button.click()
        manejo_codigo_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='mainForm:j_idt1752_data']/tr[6]/td/span")))
        manejo_codigo_button.click()
        time.sleep(3)
        driver.find_element(By.XPATH, "//*[@id='mainForm:j_idt1758']/span[2]").click()
        time.sleep(4)
        print("causales button clicked")
        print("TimeoutException: Element not found")

    driver.find_element(By.XPATH, "//*[@id='mainForm:dtAgreeGuiones_data']/tr[7]/td/span").click()
    time.sleep(4)
    driver.find_element(By.XPATH, "//span[contains(text(),'OMITIR')]").click()
    time.sleep(3)

def payment_agreement(driver, agreement_value, agreement_comment, agreement_date):
    time.sleep(4)

    agreement_comment_field = driver.find_element(By.XPATH, "//*[@id='mainForm:idObsAgreeScript']")
    agreement_comment_field.send_keys(agreement_comment)

    driver.find_element(By.XPATH, "//*[@id='mainForm:pgPanelDatosDeContacto:dtObligTogg2_data']/tr/td[2]/div/div[2]/span").click()
    time.sleep(4)
    driver.find_element(By.XPATH, "//*[@id='mainForm:pgPanelDatosDeContacto:nuevoAcuerdo']/span[2]").click()
    time.sleep(4)

    try:
        wait = WebDriverWait(driver, 5)
        skip_add_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='mainForm:j_idt12859']/span")))
        skip_add_button.click()
        time.sleep(4)
        print("Skip and add button clicked")
    except TimeoutException:
        print("TimeoutException: Element not found")

    agreement_value_field = driver.find_element(By.XPATH, "//*[@id='mainForm:idAccordionPanelAcuerdos:j_idt12884_input']")
    agreement_value_field.send_keys(agreement_value)
    time.sleep(3)

    agreement_date_field = driver.find_element(By.XPATH, "//*[@id='mainForm:idAccordionPanelAcuerdos:j_idt12888_input']")
    agreement_date_field.send_keys(agreement_date)
    time.sleep(3)
    agreement_date_field.send_keys(Keys.ENTER)
    driver.find_element(By.XPATH, "//*[@id='mainForm:idAccordionPanelAcuerdos:ingresarAcuerdo']/div[2]").click()
    time.sleep(4)

    driver.find_element(By.XPATH, "//*[@id='mainForm:idAccordionPanelAcuerdos:j_idt12892']/div[3]/span").click()
    driver.find_element(By.XPATH, "//*[@id='mainForm:idAccordionPanelAcuerdos:j_idt12892_15']").click()
    time.sleep(4)

    driver.find_element(By.XPATH, "//*[@id='mainForm:idAccordionPanelAcuerdos:j_idt12910']/div[3]/span").click()
    time.sleep(2)
    driver.find_element(By.XPATH, "//*[@id='mainForm:idAccordionPanelAcuerdos:j_idt12910_2']").click()
    time.sleep(3)

    driver.find_element(By.XPATH, "//*[@id='mainForm:idAccordionPanelAcuerdos:j_idt12923']/tbody/tr/td[2]/div/div[2]").click()
    time.sleep(2)

    driver.find_element(By.XPATH, "//*[@id='mainForm:j_idt13113']/span[2]").click()
    time.sleep(4)

    try:
        driver.find_element(By.XPATH, "//*[@id='mainForm:j_idt13106']").click()
        time.sleep(4)
    except Exception:
        driver.find_element(By.XPATH, "//*[@id='mainForm:j_idt13127']/span[2]").click()
        time.sleep(4)

if __name__ == "__main__":
    load_dotenv()
    username = os.environ.get("USERNAME_VG")
    password = os.environ.get("PASSWORD_VG")
    agreement_comment = "cobranza digital (gestiÃ³n IA)"
    
    options = Options()
    options.add_experimental_option("detach", True)

    driver = webdriver.Chrome(options=options)
    login(driver, username, password)
    select_campaign(driver)

    csv_path = r"C:\Users\jsanchez\OneDrive - VISION GERENCIAL ASESORIAS Y COBRANZAS SAS\01. Carteras VG\23. Leonisa\Cobranza digital\ARCHIVO DE COMPROMISOS PARA CARGUE (RPA)\compromisos RPA leonisa.csv"
    df = pd.read_csv(csv_path, sep=";")

    for index, row in df.iterrows():
        cedula = str(row["NIT"]).strip()
        agreement_value = str(row["VALOR"]).strip()
        agreement_date = str(row["FECHA"]).strip()
        telefono = str(row["TELEFONO"]).strip().replace(" ", "")

        try:
            client_management(driver, cedula, telefono)
            payment_agreement(driver, agreement_value, agreement_comment, agreement_date)
            df.at[index, "ESTADO"] = "Procesado"
        except Exception as e:
            df.at[index, "ESTADO"] = f"Error: {str(e)}"
            traceback.print_exc()

    df.to_csv(csv_path, sep=";", index=False, encoding="utf-8-sig")
    driver.quit()
    print("Proceso terminado correctamente")
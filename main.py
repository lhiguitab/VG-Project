from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.support.ui import WebDriverWait # Used for the wait
from selenium.webdriver.support import expected_conditions as EC # Used for the wait
from dotenv import load_dotenv
from selenium.common.exceptions import TimeoutException # Used for the try except block
import time
import pandas as pd 
import os


def login(driver, username, password):
    driver.get("https://visiong.iagree.co/iAgree/faces/login.xhtml")
    driver.maximize_window()
    time.sleep(2)  # Wait for the page to load
    assert "i Agree 2.0" in driver.title
    user = driver.find_element(By.NAME, "loginForm:j_idt22")
    user.send_keys(username)

    password_field = driver.find_element(By.NAME, "loginForm:j_idt24")
    password_field.send_keys(password)

    # Get the captcha text element
    captcha_text = driver.find_element(By.ID, "captcha") 
    captcha_input = driver.find_element(By.NAME, "loginForm:j_idt26")
    captcha_input.send_keys(captcha_text.text)
    captcha_input.send_keys(Keys.RETURN)

def select_campaign(driver):
    time.sleep(3)  # Wait for the page to load

    # # Click on the "Grupo 3" link
    # grupo_3_link = driver.find_element(By.XPATH, "//td[contains(text(), '3 | LEONISA CASTIGO')]")
    # grupo_3_link.click()

    # time.sleep(1)  # Wait for the page to load
    # grupo_3_link = driver.find_element(By.XPATH, "//*[@id='mainForm:dtCampanas:0:j_idt204']/span[1]")
    # grupo_3_link.click()

    # time.sleep(1)  # Wait for the page to load

    # # Click on the "Gestionar" link
    # manage_link = driver.find_element(By.XPATH, "//*[@id='mainForm:mnGestionar']/a")
    # manage_link.click()

    # click on the "LEONISA MASTER"
    ingresar_leonisa_link= driver.find_element(By.XPATH, "//*[@id='mainForm:j_idt106:0:j_idt112']/span")
    ingresar_leonisa_link.click()
    time.sleep(1)  # Wait for the page to load

def client_management(driver, cedula):
    time.sleep(3)

    # Search for the client by ID
    cedula_input = driver.find_element(By.XPATH, "//*[@id='topBarForm:itBuscarGenerico']")
    cedula_input.send_keys(cedula)
    # click on the search button
    driver.find_element(By.XPATH, "//*[@id='topBarForm:j_idt56_button']/span[1]").click()
    time.sleep(1)

    # Select client
    driver.find_element(By.XPATH, "//*[@id='mainForm:idDtDeudoresObligaciones_data']/tr/td[3]").click()
    time.sleep(1)

    # Select phone number
    driver.find_element(By.XPATH, "//*[@id='mainForm:pgRenderisarDatosContacto:dtTelefonosDeudorData_data']/tr[1]/td[2]").click()
    time.sleep(2)

    # Select "Contacto titular" 
    driver.find_element(By.XPATH, "//*[@id='mainForm:dtAgreeGuiones_data']/tr[11]/td/span").click()
    time.sleep(2)

    # Select keep contact
    wait = WebDriverWait(driver, 10)  # Wait until 10 secs max
    keep_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'MANTENER')]")))
    keep_button.click()
    time.sleep(2)

    # Select "Compromiso de pago"
    driver.find_element(By.XPATH, "//*[@id='mainForm:dtAgreeGuiones_data']/tr[7]/td/span").click()
    time.sleep(2)
    # Select skip 
    driver.find_element(By.XPATH, "//span[contains(text(),'OMITIR')]").click()
    time.sleep(1)

def payment_agreement(driver, agreement_value,agreement_comment, agreement_date):
    time.sleep(2)

    # add the agreement comment
    agreement_comment_field = driver.find_element(By.XPATH, "//*[@id='mainForm:idObsAgreeScript']")
    agreement_comment_field.send_keys(agreement_comment)

    #Select the payment agreement
    driver.find_element(By.XPATH, "//*[@id='mainForm:pgPanelDatosDeContacto:dtObligTogg2_data']/tr/td[2]/div/div[2]/span").click()
    time.sleep(2)

    # Select "Acuerdo"
    driver.find_element(By.XPATH, "//*[@id='mainForm:pgPanelDatosDeContacto:nuevoAcuerdo']/span[2]").click()
    time.sleep(2)

    # Select "omitir y agregar nuevo"
    try:
        wait = WebDriverWait(driver, 3)  # Wait until 2 secs max
        skip_add_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='mainForm:j_idt12859']/span")))
        skip_add_button.click()
        time.sleep(2)
        print("Skip and add button clicked")
    except TimeoutException:
        print("TimeoutException: Element not found")

    # add the agreement value
    agreement_value_field = driver.find_element(By.XPATH, "//*[@id='mainForm:idAccordionPanelAcuerdos:j_idt12884_input']")
    agreement_value_field.send_keys(agreement_value)
    time.sleep(1)

    # Selecet the date
    agreement_date_field = driver.find_element(By.XPATH, "//*[@id='mainForm:idAccordionPanelAcuerdos:j_idt12888_input']")
    agreement_date_field.send_keys(agreement_date)
    time.sleep(1)
    agreement_date_field.send_keys(Keys.ENTER)
    driver.find_element(By.XPATH, "//*[@id='mainForm:idAccordionPanelAcuerdos:ingresarAcuerdo']/div[2]").click()
    time.sleep(2)

    # Select the confirmation hour
    driver.find_element(By.XPATH, "//*[@id='mainForm:idAccordionPanelAcuerdos:j_idt12892']/div[3]/span").click()
    driver.find_element(By.XPATH, "//*[@id='mainForm:idAccordionPanelAcuerdos:j_idt12892_15']").click()
    time.sleep(2)

    # Select "Efecto Acuerdo"
    driver.find_element(By.XPATH, "//*[@id='mainForm:idAccordionPanelAcuerdos:j_idt12910']/div[3]/span").click()
    time.sleep(0.2)
    driver.find_element(By.XPATH, "//*[@id='mainForm:idAccordionPanelAcuerdos:j_idt12910_2']").click()
    time.sleep(1)

    # Select "posibilidad de cumplimiento"
    driver.find_element(By.XPATH, "//*[@id='mainForm:idAccordionPanelAcuerdos:j_idt12923']/tbody/tr/td[2]/div/div[2]").click()


if __name__ == "__main__":
    # Load environment variables from .env file
    load_dotenv()

    # Set up the driver
    # driver = webdriver.Chrome()
    # driver.get("https://visiong.iagree.co/iAgree/faces/login.xhtml")
    # driver.maximize_window()

    # Get the username and password from environment variables
    username = os.environ.get("USERNAME_VG")
    password = os.environ.get("PASSWORD_VG")
    agreement_comment = ("cobranza digital (gestión IA)")


    options = Options()
    options.add_experimental_option("detach", True)

    csv_path = r"C:\Users\57318\compromiso pruebas RPA leonisa.csv"
    df = pd.read_csv(csv_path, sep=";")

    for index, row in df.iterrows():
        cedula = str(row["NIT"]).strip()
        phone_number = str(row["TELEFONO"]).strip()
        agreement_value = str(row["VALOR"]).strip()
        agreement_date = str(row["FECHA"]).strip()
        efecto_acuerdo = str(row["EFECTO ACUERDO"]).strip()  

        try:
            # Set up the driver for each iteration
            driver = webdriver.Chrome(options=options)
            login(driver, username, password)
            select_campaign(driver)
            client_management(driver, cedula)
            payment_agreement(driver, agreement_value, agreement_comment, agreement_date)

            print(f"✅ Client {cedula} processed correctly.\n")

            

        except Exception as e:
            print(f"❌ error processing client {cedula}: {e}")
            try:
                driver.quit()
            except:
                pass

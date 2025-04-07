from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv
import time
import os

def login(driver, username, password):
    driver.get("https://visiong.iagree.co/iAgree/faces/login.xhtml")
    driver.maximize_window()
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

    # Click on the "Grupo 3" link
    grupo_3_link = driver.find_element(By.XPATH, "//td[contains(text(), '3 | LEONISA CASTIGO')]")
    grupo_3_link.click()

    time.sleep(1)  # Wait for the page to load
    grupo_3_link = driver.find_element(By.XPATH, "//*[@id='mainForm:dtCampanas:0:j_idt204']/span[1]")
    grupo_3_link.click()

    time.sleep(1)  # Wait for the page to load

    # Click on the "Gestionar" link
    manage_link = driver.find_element(By.XPATH, "//*[@id='mainForm:mnGestionar']/a")
    manage_link.click()

def client_management(driver, cedula):
    time.sleep(3)

    # Click on the "Buscar" link
    cedula_input = driver.find_element(By.XPATH, "//*[@id='topBarForm:itBuscarGenerico']")
    cedula_input.send_keys(cedula)
    driver.find_element(By.XPATH, "//*[@id='topBarForm:j_idt56_button']/span[1]").click()
    time.sleep(2)

    # Select client
    driver.find_element(By.XPATH, "//*[@id='mainForm:idDtDeudoresObligaciones_data']/tr/td[3]").click()
    time.sleep(2)

    # Select phone number
    driver.find_element(By.XPATH, "//*[@id='mainForm:pgRenderisarDatosContacto:dtTelefonosDeudorData_data']/tr[1]/td[2]").click()
    time.sleep(2)

    # Select "Contacto titular" 
    driver.find_element(By.XPATH, "//*[@id='mainForm:dtAgreeGuiones_data']/tr[11]/td/span").click()
    time.sleep(2)
    # Select keep contact
    driver.find_element(By.XPATH, "//*[@id='mainForm:j_idt12760']").click()
    time.sleep(1)

    # Select "Compromiso de pago"
    driver.find_element(By.XPATH, "//*[@id='mainForm:dtAgreeGuiones_data']/tr[7]/td/span").click()
    time.sleep(2)
    # Select skip 
    driver.find_element(By.XPATH, "//*[@id='mainForm:j_idt12768']/span").click()
    time.sleep(1)

    #Select the payment agreement
    driver.find_element(By.XPATH, "//*[@id='mainForm:pgPanelDatosDeContacto:dtObligTogg2_data']/tr/td[2]/div/div[2]/span").click()
    time.sleep(2)

    # select "Acuerdo"
    driver.find_element(By.XPATH, "//*[@id='mainForm:pgPanelDatosDeContacto:nuevoAcuerdo']/span[2]").click()


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
    cedula= os.environ.get("CEDULA_PRUEBA")

    options = Options()
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=options)

    print(username, password)

    login(driver, username, password)
    select_campaign(driver)
    client_management(driver, cedula)
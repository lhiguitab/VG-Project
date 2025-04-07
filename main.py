from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv
import time
import os

def login(driver, username, password):
    driver.get("https://visiong.iagree.co/iAgree/faces/login.xhtml")
    assert "i Agree 2.0" in driver.title
    user = driver.find_element(By.NAME, "loginForm:j_idt22")
    user.send_keys(username)

    password_field = driver.find_element(By.NAME, "loginForm:j_idt24")
    password_field.send_keys(password)

    # Get the captcha text element
    captcha_text = driver.find_element(By.ID, "captcha") 
    print(captcha_text.text)  # Print the captcha text to the console
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
    menu_button = driver.find_element(By.XPATH, "//*[@id='menu-button']")
    menu_closed = driver.find_elements(By.CLASS_NAME, "menu-button-rotate")

    if menu_closed:
        print("Menu not open, clicking to open")
        menu_button.click()
        time.sleep(1)
        manage_link = driver.find_element(By.XPATH, "//*[@id='mainForm:mnGestionar']/a")
        manage_link.click()
    else:
        print("Menu already open")
        time.sleep(1)
        manage_link = driver.find_element(By.XPATH, "//*[@id='mainForm:mnGestionar']/a")
        manage_link.click()

if __name__ == "__main__":
    # Load environment variables from .env file
    load_dotenv()

    # Set up the driver
    driver = webdriver.Chrome()

    # Get the username and password from environment variables
    username = os.environ.get("USERNAME_VG")
    password = os.environ.get("PASSWORD_VG")

    options = Options()
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=options)

    print(username, password)

    login(driver, username, password)
    select_campaign(driver)
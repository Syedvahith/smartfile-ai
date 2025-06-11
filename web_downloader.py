from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os, time

def download_zip_from_portal(download_dir="input_data/web"):
    os.makedirs(download_dir, exist_ok=True)

    chrome_options = Options()
    prefs = {"download.default_directory": os.path.abspath(download_dir)}
    chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")

    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()

    try:
        driver.get("https://yoururl")
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "Userid"))).send_keys("your_user")
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "password"))).send_keys("your_pass")
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "btn"))).click()

        time.sleep(5)
        driver.find_element(By.LINK_TEXT, "DumpData - Download").click()
        time.sleep(2)
        driver.find_element(By.LINK_TEXT, "Damage Claim Regionwise Status Download").click()
        time.sleep(2)
        driver.find_element(By.ID, "ContentPlaceHolder1_btnDownload").click()

        print(f"[Web] Files downloaded to {download_dir}")
        time.sleep(20)  # wait for ZIP to download
    except Exception as e:
        print(f"[Web] Error: {e}")
    finally:
        driver.quit()

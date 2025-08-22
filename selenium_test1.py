from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import sys
import time
import os
def main():
    if len(sys.argv) < 2:
        print("No link provided")
        sys.exit(1)
    link = sys.argv[1]
    

    try:
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        driver = webdriver.Chrome(options=options)
        wait = WebDriverWait(driver, 20)
    except Exception:
        print("Driver error")
        sys.exit(1)

    try:
        driver.get(link)
        
        element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'e1ax5wel2')))
        print(element.text)
        element.click()
        print("Household link clicked successfully")  
    except TimeoutException:
        print("Timeout while waiting for the element")
    except Exception:
        print("Error clicking button")
    finally:
        time.sleep(2)
        driver.quit()

if __name__ == "__main__":
    main()

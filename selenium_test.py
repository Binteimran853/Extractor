from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
import sys
import time
from selenium import webdriver

def main():
    if len(sys.argv) < 2:
        print("No link provided.")
        sys.exit(1)
    link = sys.argv[1]

    print(f"Opening link: {link}")
    try:
        driver = webdriver.Chrome()  
        wait = WebDriverWait(driver, 20)  
    except Exception as e:
        print("Error starting WebDriver:", e)
        sys.exit(1)

    try:
        driver.get(link)
        element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'challenge-code')))
        info = element.text
        print("Challenge code found:", info)
    except TimeoutException:
        print("Timeout: challenge-code element not found.")
    except Exception as e:
        print("Error during Selenium execution:", e)
    finally:
        time.sleep(10) 
        driver.quit()

if __name__ == "__main__":
    main()
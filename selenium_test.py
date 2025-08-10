from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
import sys
import time
from selenium import webdriver

def main():
    if len(sys.argv) < 2:
        print("")  # Print nothing or empty string if no link
        sys.exit(1)
    link = sys.argv[1]

    try:
        driver = webdriver.Chrome()  
        wait = WebDriverWait(driver, 20)  
    except Exception as e:
        print("")  # Print nothing if error starting driver
        sys.exit(1)

    try:
        driver.get(link)
        element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'challenge-code')))
        info = element.text
        print(info)  
    except TimeoutException:
        print("") 
    except Exception as e:
        print("") 
    finally:
        time.sleep(2)  
        driver.quit()

if __name__ == "__main__":
    main()

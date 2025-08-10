from selenium import webdriver
from selenium.webdriver.common.by import By
import time
driver = webdriver.Chrome()  
driver.get('http://127.0.0.1:8000/netflix-otp/')  

time.sleep(3)
anchor = driver.find_element(By.TAG_NAME, 'a')

# Extract href attribute
href = anchor.get_attribute('href')
print(f'Extracted link: {href}')

driver.get(href)

time.sleep(3)


info = driver.find_element(By.CLASS_NAME, 'latest-opt').text
print(f'Extracted info: {info}')


driver.quit()

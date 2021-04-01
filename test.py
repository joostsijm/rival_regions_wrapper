
import time

from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

options = webdriver.ChromeOptions()
# "--headless"options.add_argument("--headless")
options.add_argument("user-agent=DN")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
driver = webdriver.Chrome(options=options)
stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
    )

USERNAME = ''
PASSWORD = ''
            
time.sleep(3)
driver.get('http://rivalregions.com/')
time.sleep(2)
driver.find_element_by_xpath('//*[@id="sa_add2"]/div[2]/a[2]/div').click()
time.sleep(0.5)
driver.find_element_by_id('Email').send_keys(USERNAME)
print('SENT EMAIL LOGIN ')
time.sleep(0.5)
driver.find_element_by_xpath('/html/body/div/div[2]/div[2]/div[1]/form/div/div/input').click()
time.sleep(0.5)
driver.find_element_by_id('password').send_keys(PASSWORD)
print('SENT PASSWORD LOGIN ')
driver.find_element_by_id('submit').click()
print('SUCCESSFULLY LOGGED IN ')

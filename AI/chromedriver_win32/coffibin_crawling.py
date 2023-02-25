import time


from selenium import webdriver
from selenium.webdriver.common.by import By

wd = webdriver.Chrome('/chromedriver.exe')
wd.get("https://www.coffeebeankorea.com/store/store.asp")

wd.execute_script("storePop2('31')")

time.sleep(10)

text = wd.find_element(By.XPATH, r'//*[@id="matizCoverLayer0Content"]/div/div/div[2]/table/tbody[1]/tr[3]/td').text
print(text)
while (True):
    pass


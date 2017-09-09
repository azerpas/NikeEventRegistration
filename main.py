from selenium import webdriver
import BeautifulSoup
import requests
import os , time , random , datetime

url = "https://store.nike.com/fr/fr_fr/?l=shop,login"

event = "https://www.nike.com/events-registration/event?id=86381"

mail = ""
password = ""

identity = {'fname':'','lastname':'','mail':'abc@gmail.com','country':'france','size':["8","41"]}
fill_infos_new_account = False

driver = webdriver.Chrome()

driver.get(url)

driver.find_element_by_xpath("""//*[@id="nike-unite-loginForm"]/div[2]/input""").send_keys(mail)
driver.find_element_by_xpath("""//*[@id="nike-unite-loginForm"]/div[3]/input""").send_keys(password)
driver.find_element_by_xpath("""//*[@id="nike-unite-loginForm"]/div[6]/input""").click()

time.sleep(5)

driver.get(event)

#button register
try: 
	driver.find_element_by_xpath("""//*[@id="module-list"]/div[6]/div/button[2]""").click()
	time.sleep(2)
except Exception as e: 
	print(e)

# No need to fill these infos as they're established during account creation, but you can still use it
#if fill_infos_new_account == True:
#	driver.find_element_by_xpath("""//*[@id="field1"]""").send_keys(identity['fname'])
#	driver.find_element_by_xpath("""//*[@id="field2"]""").send_keys(identity['lastname'])
#	driver.find_element_by_xpath("""//*[@id="field3"]""").send_keys(identity['mail'])

#gender
try:
	driver.find_element_by_xpath("""field6-male""").click() #field6-female for female account
except Exception as e:
	print(e)

#country dropdown
for option in driver.find_elements_by_tag_name('option'):
	if identity['country'].lower() in option.text.lower():
		option.click()
		break
#size dropdown
for option in driver.find_elements_by_tag_name('option'):
	for size in identity['size']:
		if size.lower() in option.text.lower():
			option.click()
			break
time.sleep(1)
driver.find_element_by_xpath("""field27""").click()
driver.find_element_by_xpath("""//*[@id="module-list"]/div[6]/div/button[2]""").click()

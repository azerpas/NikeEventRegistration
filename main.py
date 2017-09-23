# coding=utf-8
from selenium import webdriver
import BeautifulSoup
import requests
import json
import os , time , random , datetime


# FR LINK
loginurl = "https://store.nike.com/fr/fr_fr/?l=shop,login"

# put your links in here
eventURLs = ['']

#identity = {'fname':'yo','lastname':'man','mail':'yoman@gmail.com','country':'','size':["8","41"]}
#fill_infos_new_account = False

driver = webdriver.Chrome()

def login(email,password):
	driver.delete_all_cookies()
	driver.get(loginurl)

	time.sleep(3)
	driver.find_element_by_xpath("""/html/body/div[11]/div[1]/div/div/div/div[1]/div[2]/div[3]/button[2]""").click()
	driver.find_element_by_xpath("""//*[@id="nike-unite-loginForm"]/div[2]/input""").send_keys(email)
	driver.find_element_by_xpath("""//*[@id="nike-unite-loginForm"]/div[3]/input""").send_keys(password)
	driver.find_element_by_xpath("""//*[@id="nike-unite-loginForm"]/div[6]/input""").click()

	time.sleep(5)
	print('Log ind')

def participate(urlof,sizee,sexof,phone):
	
	driver.get(urlof)

	time.sleep(5)
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
	# execute_script("document.get...blablabla") -> JAVASCRIPT TO CHANGE VALUE
	#gender
	if sexof == 'f':
		try:
			driver.find_element_by_xpath("""//*[@id="field6-female"]""").click() 
		except Exception as e:
			print(e)
	else:
		try:
			driver.find_element_by_xpath("""//*[@id="field6-male"]""").click() #field6-female for female account
		except Exception as e:
			print(e)

	if phone != "":
		print(phone)
		print("Changing phone number")
		driver.find_element_by_xpath("""//*[@id="field4"]""").send_keys(phone)
	try:
		driver.execute_script("machin = document.getElementById('field4').value;")
		driver.execute_script("machin = '' + machin;")
		driver.execute_script("document.getElementById('field4').value = machin;")
	except Exception as e:
		print(e)
		time.sleep(10)
		print("Can't change number")
	try:
		driver.find_element_by_xpath("""//*[@id="module-list"]/div[6]/div/div[1]/form/div[8]/div[1]/a""").click()
	except Exception as e:
		print (e)

	try:
		driver.find_element_by_xpath("""//*[@id="module-list"]/div[6]/div/div[1]/form/div[8]/div[1]/ul/li[%d]""" % sizee).click()
	except Exception as e:
		print(e)
	# [2] = size 7
			
	time.sleep(1)
	try:
		driver.find_element_by_xpath("""//*[@id="module-list"]/div[6]/div/div[1]/form/div[11]/div/div[1]/input""").click()
	except Exception as e:
		driver.find_element_by_xpath("""//*[@id="module-list"]/div[6]/div/div[1]/form/div[10]/div/div[1]/input""").click()
	time.sleep(1)
	driver.find_element_by_xpath("""//*[@id="module-list"]/div[6]/div/button[2]""").click()
	time.sleep(8)
	print("Sur la liste pour evenement:")
	print(urlof)

def main():
	while True:
		theMail = raw_input("Input the mail:\n")
		thePass = raw_input("Input the password:\n")
		theSex = raw_input("Input the sex: f or m\n")
		thePhone = raw_input("Input the phone, for no phone, empty value\n")
		if theSex == 'f':
			sizee = random.choice([1,2])
			# realistic choice for a girl
		else:
			sizee = random.choice([3,4,5,6,7,8,9,10])
			# realistic choice for a boy
		login(theMail,thePass)
		for event in eventURLs:
			participate(event,sizee,theSex,thePhone)
		print("Account: " + str(theMail) + " registered for the event\n")
		print("To create the next account, press any key, or exit the program\n")
		# Created to manually change the IP, unless you have residential proxies, Nike strong against proxies
		raw_input("Tap:\n")

main()


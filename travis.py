# coding=utf-8
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
import zipfile
import BeautifulSoup
import requests
import json
import os , time , random , datetime
from splinter import Browser


####### CHANGE URLS HERE #########

loginurl = "https://store.nike.com/fr/fr_fr/?l=shop,login"

eventURLs = ["https://www.nike.com/events-registration/event?id=93464"]

def co(proxy):

	manifest_json = """
{
    "version": "1.0.0",
    "manifest_version": 2,
    "name": "Chrome Proxy",
    "permissions": [
        "proxy",
        "tabs",
        "unlimitedStorage",
        "storage",
        "<all_urls>",
        "webRequest",
        "webRequestBlocking"
    ],
    "background": {
        "scripts": ["background.js"]
    },
    "minimum_chrome_version":"22.0.0"
}
"""

	background_js = """
var config = {
        mode: "fixed_servers",
        rules: {
          singleProxy: {
            scheme: "http",
            host: "XXXHOSTXXX",
            port: parseInt(XXPORTXX)
          },
          bypassList: ["foobar.com"]
        }
      };

chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

function callbackFn(details) {
    return {
        authCredentials: {
            username: "XXUSXX",
            password: "XXPWDXX"
        }
    };
}

chrome.webRequest.onAuthRequired.addListener(
            callbackFn,
            {urls: ["<all_urls>"]},
            ['blocking']
);
"""

	background_js = background_js.replace('XXXHOSTXXX',proxy['host']).replace('XXPORTXX',proxy['port']).replace('XXUSXX',proxy['usr']).replace('XXPWDXX',proxy['pwd'])


	pluginfile = 'proxy_auth_plugin.zip'

	with zipfile.ZipFile(pluginfile, 'w') as zp:
		zp.writestr("manifest.json", manifest_json)
		zp.writestr("background.js", background_js)

	co = Options()
	co.add_argument("--start-maximized")
	co.add_extension(pluginfile)
	prefs = {"profile.managed_default_content_settings.images":2}
	co.add_experimental_option("prefs",prefs)
	return co


def login(driver,email,password):
	driver.delete_all_cookies()
	driver.get(loginurl)

	time.sleep(3)
	try:
		driver.find_element_by_xpath("""/html/body/div[11]/div[1]/div/div/div/div[1]/div[2]/div[3]/button[2]""").click()
	except:
		pass
	driver.find_element_by_xpath("""//*[@id="nike-unite-loginForm"]/div[2]/input""").send_keys(email)
	driver.find_element_by_xpath("""//*[@id="nike-unite-loginForm"]/div[3]/input""").send_keys(password)
	driver.find_element_by_xpath("""//*[@id="nike-unite-loginForm"]/div[6]/input""").click()

	time.sleep(5)
	print('Logged')

def participate(driver,urlof,sizee,phone):

	driver.get(urlof)

	time.sleep(5)
	try:
		driver.find_element_by_xpath("""/html/body/div[11]/div[1]/div/div/div/div[1]/div[2]/div[3]/button[2]""").click()
	except:
		pass
    
	#button register
	try: 
		driver.find_element_by_xpath("""//*[@id="module-list"]/div[6]/div/button[2]""").click()
		time.sleep(2)
	except Exception as e: 
		print("ERROR 4")
	

	try:
		driver.find_element_by_xpath("""//*[@id="module-list"]/div[6]/div/div[1]/form/div[2]/div[1]/a""").click()
	except Exception as e:
		time.sleep(10)

		driver.find_element_by_xpath("""//*[@id="module-list"]/div[6]/div/div[1]/form/div[2]/div[1]/a/span[2]""").click()

	try:
		driver.find_element_by_xpath("""//*[@id="module-list"]/div[6]/div/div[1]/form/div[2]/div[1]/ul/li[%d]""" % sizee).click()
	except Exception as e:
		print("ERROR with size")
			
	time.sleep(1)
	try:
		driver.find_element_by_xpath("""//*[@id="module-list"]/div[6]/div/div[1]/form/div[5]/div/div[1]/input""").click()
	except Exception as e:
		print("ERROR 5")
		try:
			driver.find_element_by_xpath("""//*[@id="module-list"]/div[6]/div/div[1]/form/div[5]/div/div[1]""").click()
		except:
			driver.execute_script("""document.getElementById("field26").click()""")

	time.sleep(1)
	driver.find_element_by_xpath("""//*[@id="module-list"]/div[6]/div/button[2]""").click()
	time.sleep(8)
	print("On the list for:")
	print(urlof)

def main():
  #debug#
  errors = []
  ######
  ## accounts need to be formatted like this : {'mail':'mike@gmail.com','password':'mike123','+44.......'}
  accounts = []
  ## proxies need to be formatted like this : {'host':'192.1.1.1','port':3232,'usr':'username','pwd':'password'}
  proxies = []
  
  while True:
		for p in accounts:
			theMail = p['mail']
			thePass = p['password']
			thePhone = p['no']
			#choosing random size - travis is 8 US to 12 US, 8 sizes so 1 to 8
      sizee = random.choice([1,2,3,4,5,6,7,8])
			proxy = random.choice(proxies)
			proxies.remove(proxy)
			cp = co(proxy)
			driver = webdriver.Chrome("/yourPATH",chrome_options=cp)
			try:
				login(driver,theMail,thePass)
				for event in eventURLs:
					participate(driver,event,sizee,thePhone)
          print("Account: " + str(theMail) + " registered\n")
			except Exception as e:
				print(e)
				print('Account cannot be logged in or registered')
				errors.append(p)
			driver.close()
      
	print(errors)

main()


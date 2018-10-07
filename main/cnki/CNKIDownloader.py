from selenium import webdriver
from time import sleep
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import xlrd
import traceback
import selenium.webdriver.support.ui as ui
import os

# set the WebDriver browser
fp = webdriver.FirefoxProfile()
fp.set_preference("browser.download.folderList", 2)
fp.set_preference("browser.download.manager.showWhenStarting", False)
fp.set_preference("browser.download.dir", "")
fp.set_preference("pdfjs.disabled", True)
fp.set_preference("plugin.disable_full_page_plugin_for_types", "application.pdf")
fp.set_preference("browser.helperApps.neverAsk.openFile", "application/pdf")
fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/pdf")
fp.set_preference("browser.helperApps.alwaysAsk.force", False)
driver = webdriver.Firefox(firefox_profile=fp)

# login into CNKI
login_url = 'http://kns.cnki.net/kns/logindigital.aspx?ParentLocation=http://www.cnki.net'
username = ''
password = ''
driver.get(login_url)
sleep(3)
driver.find_element_by_xpath('//input[@id="username"]').send_keys(username)
driver.find_element_by_xpath('//input[@id="password"]').send_keys(password)
driver.find_element_by_class_name('login').click()
sleep(3)
print('Logged in!')

# load the journal article links
path = ''
file = 'cnki_tsqbgz_2016_21.txt'
file_path = os.path.join(path, file)
with open(file_path, encoding='utf-8') as f:
    count = 0
    for link in f.readlines():
        count += 1
        if count <= 0:
           continue
        if count % 500 == 0:
            sleep(600)
        try:
            driver.get(link)
            sleep(15)
            title_name_xpath = '//h2[@class="title"]'
            title_name = driver.find_element_by_xpath(title_name_xpath).text
            print(title_name)
            driver.execute_script("window.scrollBy(0,3000)")
            sleep(5)
            driver.find_element_by_xpath('//*[@id="pdfDown"]').click()
            sleep(10)
        except:
            driver.delete_all_cookies()
            sleep(20)
        print(str(count) + ' articles have been processed!')





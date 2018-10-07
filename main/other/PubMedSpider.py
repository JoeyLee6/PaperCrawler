from selenium import webdriver
from time import sleep
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import xlrd
import traceback

# set urls
path = ''
urls = list()
link_path = path + '/altmetrics_clinical_top100.xlsx'
workbook = xlrd.open_workbook(link_path)
booksheet = workbook.sheet_by_name('Sheet2')
cols = booksheet.col_values(colx=0, start_rowx=0)
urls.extend(cols)
print('Number of URLs:', len(urls))

# set Firefox Preferences
fp = webdriver.FirefoxProfile()
fp.set_preference("browser.download.folderList", 2)
fp.set_preference("browser.download.manager.showWhenStarting", False)
fp.set_preference("browser.download.dir", "")
fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/xml")
driver = webdriver.Firefox(firefox_profile=fp)

# get the Bib
count = 0
for url in urls:
    try:
        driver.delete_all_cookies()
        driver.get(url)
        sleep(5)
        driver.find_element_by_xpath('//a[@sourcecontent="send_to_menu"]').click()
        sleep(1)
        driver.find_element_by_xpath('//input[@id="dest_File"]').send_keys(Keys.SPACE)
        sleep(1)
        select_format = Select(driver.find_element_by_xpath('//select[@id="file_format"]'))
        sleep(1)
        select_format.select_by_value('xml')
        sleep(1)
        driver.find_element_by_xpath('//div[@class="submenu file"]/button').click()
        sleep(5)
        count += 1
        print('Processed:', count)
    except:
        traceback.print_exc()
        sleep(30)
        continue

sleep(60)
driver.close()
from selenium import webdriver
from time import sleep
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import xlrd
import traceback
import csv

# set urls
urls = [
    'http://s.wanfangdata.com.cn/Paper.aspx?q=刊名%3a"情报杂志"+日期%3a2010-2017+DBID%3aWF_QK+期刊id%3aqbzz&f=kan'
    # 'http://s.wanfangdata.com.cn/Paper.aspx?q=刊名%3A"情报科学"+DBID%3aWF_QK+日期%3a2010-2011&f=sort&o=sortby+date'
]

# set firefox preferences
fp = webdriver.FirefoxProfile()
fp.set_preference("browser.download.folderList", 2)
fp.set_preference("browser.download.manager.showWhenStarting", False)
fp.set_preference("browser.download.dir", "")
fp.set_preference("pdfjs.disabled", True)
fp.set_preference("plugin.disable_full_page_plugin_for_types", "application.pdf")
fp.set_preference("browser.helperApps.neverAsk.openFile", "application/pdf")
fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/pdf")
fp.set_preference("browser.helperApps.alwaysAsk.force", False)
# fp.set_preference("browser.download.manager.alertOnEXEopen", False)
# fp.set_preference("browser.download.manager.focusWhenStarting", False)
# fp.set_preference("browser.download.manager.useWindow", False)
# fp.set_preference("browser.download.manager.showAlertOnComplete", False)
# fp.set_preference("browser.download.manager.closewhenDone", False)
driver = webdriver.Firefox(firefox_profile=fp)




# search papers
for url in urls:
    # create csv file
    # writer = csv.writer(open(keyword + '.csv', 'w', encoding='utf-8', newline=''))
    # writer.writerow(['Number', 'Title', 'Issue', 'Author'])

    # search the journal
    count = 0
    driver.get(url)
    sleep(5)

    while True:
        search_page = driver.current_url
        print('Current Search Page:', search_page)
        article_links_a = driver.find_elements_by_xpath('//a[@class="download"]')
        article_links = list()
        for article_link_a in article_links_a:
            article_links.append(article_link_a.get_attribute('href'))
        for article_link in article_links:
            count += 1
            driver.delete_all_cookies()
            print('Article', count, ':', article_link)
            driver.get(article_link)
            sleep(3)
        driver.get(search_page)
        sleep(5)
        page_links_a = driver.find_elements_by_xpath('//a[@class="page"]')
        page_links_text = list()
        for page_link_a in page_links_a:
            page_links_text.append(page_link_a.text)
        if '下一页>>' in page_links_text:
            next_page = driver.find_element_by_xpath('//a[@class="page" and text()="下一页>>"]').get_attribute('href')
            driver.get(next_page)
            if 'sorry.html' in driver.current_url:
                print()
                print('Error! Sleep for 60 seconds!')
                driver.delete_all_cookies()
                sleep(60)
                driver.get(next_page)
            print()
            sleep(5)
        else:
            break

print('Wait for downloading, sleep 300 seconds')
sleep(300)
driver.close()

from selenium import webdriver
from time import sleep
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import xlrd
import traceback
import csv

fp = webdriver.FirefoxProfile()
driver = webdriver.Firefox()

urls = []
with open('./emergency.txt') as f:
    for line in f.readlines():
        urls.append(line.replace('\n', '').replace('锘縣', 'h'))

for url in urls:
    driver.get(url)
    sleep(5)
    keywords_list_xpath = '//div[@class="fixed-width baseinfo-feild"]/div[@class="row row-keyword"]/span[@class="text"]/a'
    keywords = list()
    for i in range(len(driver.find_elements_by_xpath(keywords_list_xpath))):
        keywords_xpath = keywords_list_xpath + '[' + str(i + 1) + ']'
        try:
            element = driver.find_element_by_xpath(keywords_xpath)
        except:
            continue
        keywords.append(element.text)
    keywords_str = ' '.join(keywords).replace('  ', ' ')
    print('Keywords: %s' % keywords_str)

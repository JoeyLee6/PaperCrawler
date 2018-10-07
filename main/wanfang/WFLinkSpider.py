from selenium import webdriver
from time import sleep
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import xlrd
import traceback
import selenium.webdriver.support.ui as ui
import os
import re

os.chdir('')

link = 'http://c.wanfangdata.com.cn/Periodical-qbxb.aspx'

driver = webdriver.Firefox()
driver.delete_all_cookies()

driver.get(link)
sleep(3)

years_xpath = '//div[@class="new_ul"]/ul/li'

output_file = './qbxb_2003_2001.txt'

years_elements = driver.find_elements_by_xpath(years_xpath)
error_count = 0
with open(output_file, 'w', encoding='utf-8') as f:
    for i in range(3):
        year_xpath = years_xpath + '[' + str(i + 15) + ']'
        driver.find_element_by_xpath(year_xpath + '/a/t').click()
        sleep(10)
        volumes_xpath = year_xpath + '/p/a'
        for j in range(len(driver.find_elements_by_xpath(volumes_xpath))):
            volume_xpath = volumes_xpath + '[' + str(j + 1) + ']'
            try:
                driver.find_element_by_xpath(volume_xpath).click()
            except Exception as e:
                print(e)
                error_count += 1
                if error_count % 5 == 0:
                    error_count = 0
                    print('Error at volume path i: %d, j: %d' % (i, j))
                else:
                    j -= 1
                continue
            sleep(10)
            articles_xpath = '//div[@class="Content_div_detail"]/ul/li'
            for k in range(len(driver.find_elements_by_xpath(articles_xpath))):
                try:
                    article_xpath = articles_xpath + '[' + str(k + 1) + ']'
                    article_link_xpath = article_xpath + '/a[@class="qkcontent_name"]'
                    article_link = driver.find_element_by_xpath(article_link_xpath).get_attribute('href')
                    f.write(article_link)
                    f.write('\n')
                except Exception as e:
                    print(e)
                    print('i: %d, j: %d, k: %d' % (i, j, k))
                    sleep(10)
                    continue
    f.flush()
    f.close()
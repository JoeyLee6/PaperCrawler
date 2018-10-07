from selenium import webdriver
from time import sleep
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import xlrd
import traceback
import selenium.webdriver.support.ui as ui
import os
import re

driver = webdriver.Firefox()

driver.delete_all_cookies()
driver.get('http://www.baidu.com')
sleep(3)


# load the journal article links
os.chdir('')
path = './links'
file = 'xdtsqbjs_2003_2001.txt'
output_path = './xdtsqbjs_2003_2001'
file_path = os.path.join(path, file)

error_links_list = list()

links_set = set()
duplicate_times = 0

with open(file_path, encoding='utf-8') as f1:
    count = 0
    for link in f1.readlines():
        link = link.replace('\n', '').replace('\ufeff', '')
        count += 1
        if count % 100 == 0:
            driver.delete_all_cookies()
            sleep(60)
        if link in links_set:
            print('\nduplicate link at count %d!' % count)
            duplicate_times += 1
            print('duplicate %d times!' % duplicate_times)
            continue
        links_set.add(link)
        try:
            print('\nNumber: %d' % count)
            driver.get(link)
            sleep(10)
            journal = '情报学报'
            print('Journal: %s' % journal)
            year = link.split('_')[1][4:8]
            issue = link.split('_')[1][8:10]
            print('Year: %s' % year)
            print('Issue: %s' % issue)
            authors = str()
            authors_xpath = '//div[@class="fixed-width baseinfo-feild"]/div[@class="row row-author"]/span[@class="text"]/a'
            for i in range(len(driver.find_elements_by_xpath(authors_xpath))):
                author_xpath = authors_xpath + '[' + str(i + 1) + ']'
                authors += (driver.find_element_by_xpath(author_xpath).text + ' ')
            authors = authors.strip()
            print('Authors: %s' % authors)
            title_xpath = '//div[@class="section-baseinfo"]/h1'
            title = driver.find_element_by_xpath(title_xpath).text.strip()
            print('Title: %s' % title)
            abstract_xpath = '//div[@class="baseinfo-feild abstract"]/div[@class="row clear zh"]/div[@class="text"]'
            abstract = driver.find_element_by_xpath(abstract_xpath).text.strip()
            print('Abstract: %s' % abstract)
            keywords_list_xpath = '//div[@class="fixed-width baseinfo-feild"]/div[@class="row row-keyword"]/span[@class="text"]/a'
            keywords_list = list()
            for i in range(len(driver.find_elements_by_xpath(keywords_list_xpath))):
                keywords_xpath = keywords_list_xpath + '[' + str(i + 1) + ']'
                try:
                    element = driver.find_element_by_xpath(keywords_xpath)
                except:
                    continue
                keywords_list.append(element.text)
            keywords = ' '.join(keywords_list).replace('  ', ' ')
            print('Keywords: %s' % keywords)
            if '@' in keywords:
                print('Contains no keywords!')
                continue
            print('Link: %s' % link)
            filename = str(count) + '.txt'
            output_file_path = output_path + '/' + filename
            with open(output_file_path, 'w', encoding='utf-8') as f:
                f.write('Journal|')
                f.write(journal)
                f.write('\n')
                f.write('Year|')
                f.write(year)
                f.write('\n')
                f.write('Issue|')
                f.write(issue)
                f.write('\n')
                f.write('Authors|')
                f.write(authors)
                f.write('\n')
                f.write('Title|')
                f.write(title)
                f.write('\n')
                f.write('Abstract|')
                f.write(abstract)
                f.write('\n')
                f.write('Keywords|')
                f.write(keywords)
                f.write('\n')
                f.write('Link|')
                f.write(link)
                f.write('\n')
                f.flush()
                f.close()
        except Exception as e:
            driver.delete_all_cookies()
            print(e)
            print('Error at count number %d' % count)
            error_links_list.append(link)
            sleep(30)







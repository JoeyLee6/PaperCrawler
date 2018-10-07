from selenium import webdriver
from time import sleep
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import xlrd
import traceback
import selenium.webdriver.support.ui as ui
import os
import re

# set the WebDriver browser
# fp = webdriver.FirefoxProfile()
# fp.set_preference("browser.download.folderList", 2)
# fp.set_preference("browser.download.manager.showWhenStarting", False)
# fp.set_preference("browser.download.dir", "")
# fp.set_preference("pdfjs.disabled", True)
# fp.set_preference("plugin.disable_full_page_plugin_for_types", "application.pdf")
# fp.set_preference("browser.helperApps.neverAsk.openFile", "application/pdf")
# fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/pdf")
# fp.set_preference("browser.helperApps.alwaysAsk.force", False)
driver = webdriver.Firefox()

# login into CNKI
driver.delete_all_cookies()
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
os.chdir('')
path = './links'
file = 'qbzlgz_2003_2001.txt'
output_path = './qbzlgz_2003_2001'
file_path = os.path.join(path, file)

links_list = list()
journal_list = list()
year_list = list()
issue_list = list()
authors_list = list()
title_list = list()
abstract_list = list()
keywords_list = list()

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
            sleep(30)
        if link in links_set:
            print('\nduplicate link at count %d!' % count)
            duplicate_times += 1
            print('duplicate %d times!' % duplicate_times)
            continue
        links_set.add(link)
        try:
            print('\nNumber: %d' % count)
            driver.get(link)
            sleep(3)
            journal_xpath = '//div[@class="wxsour"]/div[@class="sourinfo"]/p[@class="title"]/a'
            journal = driver.find_element_by_xpath(journal_xpath).text
            print('Journal: %s' % journal)
            sources_xpath = '//div[@class="wxsour"]/div[@class="sourinfo"]/p'
            has_year_issue = False
            year = str()
            issue = str()
            for i in range(len(driver.find_elements_by_xpath(sources_xpath))):
                p_a_xpath = '//div[@class="wxsour"]/div[@class="sourinfo"]/p[' + str(i + 1) + ']/a'
                text = ''
                try:
                    text = driver.find_element_by_xpath(p_a_xpath).text
                except:
                    continue
                if '年' in text and '期' in text:
                    has_year_issue = True
                    year += text[:4]
                    issue += text[4:].replace('年', '').replace('期', '')
                if has_year_issue:
                    break
            print('Year: %s' % year)
            print('Issue: %s' % issue)
            authors = str()
            authors_xpath = '//div[@class="author"]/span'
            for i in range(len(driver.find_elements_by_xpath(authors_xpath))):
                author_xpath = authors_xpath + '[' + str(i + 1) + ']/a'
                authors += (driver.find_element_by_xpath(author_xpath).text + ' ')
            authors = authors.strip()
            print('Authors: %s' % authors)
            title_xpath = '//h2[@class="title"]'
            title = driver.find_element_by_xpath(title_xpath).text
            print('Title: %s' % title)
            abstract_xpath = '//span[@id="ChDivSummary"]'
            abstract = driver.find_element_by_xpath(abstract_xpath).text
            print('Abstract: %s' % abstract)
            keywords_list_xpath = '//div[@class="wxInfo"]/div[@class="wxBaseinfo"]/p'
            len_parts = len(driver.find_elements_by_xpath(keywords_list_xpath))
            has_keywords = False
            keywords = str()
            for i in range(len_parts):
                label_xpath = keywords_list_xpath + '[' + str(i + 1) + ']/label'
                if '关键词' in driver.find_element_by_xpath(label_xpath).text:
                    has_keywords = True
                    keywords_xpath = keywords_list_xpath + '[' + str(i + 1) + ']/a'
                    for j in range(len(driver.find_elements_by_xpath(keywords_xpath))):
                        keyword = driver.find_element_by_xpath(keywords_xpath + '[' + str(j + 1) + ']').text
                        keyword = keyword.replace(';', '').replace(',', '').replace('；', '').replace(' ', '')
                        keywords += (keyword + ' ')
                if has_keywords:
                    break
            keywords = keywords.strip()
            print('Keywords: %s' % keywords)
            print('Link: %s' % link)
            if has_keywords and has_year_issue:
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
            else:
                print('has_keywords or has_year_issue is false!')
            sleep(2)
        except Exception as e:
            driver.delete_all_cookies()
            print(e)
            print('\nError at count number %d' % count)
            error_links_list.append(link)
            sleep(10)

# # output error links
# error_filename = 'error.txt'
# error_file_path = os.path.join(output_path, error_filename)
# with open(error_file_path, 'w', encoding='utf-8') as f:
#     for i in range(len(error_links_list)):
#         f.write(error_links_list[i])
#         f.write('\n')
#     f.flush()
#     f.close()










"""
Crawl the article links of specified articles
"""

from selenium import webdriver
from time import sleep
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import xlrd
import traceback
import selenium.webdriver.support.ui as ui

# set urls
path = ''

# set Firefox Preferences
fp = webdriver.FirefoxProfile()
fp.set_preference("browser.download.folderList", 2)
fp.set_preference("browser.download.manager.showWhenStarting", False)
fp.set_preference("browser.download.dir", "")
fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/xml")
fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/pdf")
fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/caj")
driver = webdriver.Firefox(firefox_profile=fp)
# driver = webdriver.PhantomJS()


# set the username and password of baidu scholar
baidu_username = ''
baidu_password = ''

# login into baidu scholar
driver.get('https://passport.baidu.com/v2/?login')
sleep(10)
driver.find_element_by_xpath('//input[@id="TANGRAM__PSP_3__userName"]').send_keys(baidu_username)
driver.find_element_by_xpath('//input[@id="TANGRAM__PSP_3__password"]').send_keys(baidu_password)
driver.find_element_by_xpath('//input[@id="TANGRAM__PSP_3__submit"]').click()
sleep(3)

# set the username and password of CNKI
CNKI_username = ''
CNKI_password = ''

# set the parameters
begin_year = 2016
end_year = 2016
journals = [
    # 情报科学
    # 'http://xueshu.baidu.com/usercenter/data/journal?cmd=journal_page&entity_id=5f43f47ec5603290b1d1908d3f90c814',
    # 情报杂志
    # 'http://xueshu.baidu.com/usercenter/data/journal?cmd=journal_page&entity_id=f6d0498c9a1e453e3d8ccf3553e34b00'
    # 情报理论与实践
    # 'http://xueshu.baidu.com/usercenter/data/journal?cmd=journal_page&entity_id=0fa62daf6b227f7c624d42a87cbd5af4'
    # 情报资料工作
    'http://xueshu.baidu.com/usercenter/data/journal?cmd=journal_page&entity_id=aa3bf9831455cd20c2a538ae70e96b07'
    # 图书情报知识
    # 'http://xueshu.baidu.com/usercenter/data/journal?cmd=journal_page&entity_id=c8456e59a6d69d52d9c3cbb73ffcb956'
    # 图书与情报
    # 'http://xueshu.baidu.com/usercenter/data/journal?cmd=journal_page&entity_id=3bbbd27f5e2ababade074e3496532266'
    # 现代情报
    # 'http://xueshu.baidu.com/usercenter/data/journal?cmd=journal_page&entity_id=e19715e7e47089a06692548dd697f4fa'
    # 现代图书情报技术
    # 'http://xueshu.baidu.com/usercenter/data/journal?cmd=journal_page&entity_id=7e28f35d24398c89cbff2cb0db26e76f'
    # 图书情报工作
    # 'http://xueshu.baidu.com/usercenter/data/journal?cmd=journal_page&entity_id=deab8bc3fb25b687269473032b5d81d8'
    # 情报学报
    # 'http://xueshu.baidu.com/usercenter/data/journal?cmd=journal_page&entity_id=83eabd46f92e9c5fcac01288b892b87c'
]
article_links_dict = dict()
article_links = list()

# iterate journals
for journal in journals:
    driver.get(journal)
    try:
        driver.find_element_by_xpath('//*[@id="content"]/div[2]/div[2]/div[1]/div[1]/div[3]/a[2]/i').click()
        sleep(3)
        driver.find_element_by_xpath('//*[@id="content"]/div[2]/div[2]/div[1]/div[1]/div[3]/a[2]/i').click()
        sleep(3)
    except:
        exit(0)
    # iterate years
    years = driver.find_elements_by_xpath('//div[@class="fre_year"]')
    for i in range(3):
        year_xpath = '//div[@class="fre_year"][' + str(i + 1) + ']'  # year 0 + ?
        driver.find_element_by_xpath(year_xpath).click()
        volumes = driver.find_elements_by_xpath(year_xpath + '/div[@class="fre_year_num"]/a')
        # iterate volumes
        for j in range(len(volumes)):
            volume_xpath = year_xpath + '/div[@class="fre_year_num"]/a[' + str(j + 1) + ']'  # journal volume 0 + ?
            try:
                print('Year: %d, Volume: %d' % ((2003 - i), (j + 1)))
                driver.find_element_by_xpath(volume_xpath).click()
                sleep(2)
            except:
                print('error!')
                sleep(30)
                continue
            while True:
                # iterate articles
                articles_xpath = '//div[@class="paper_content"]/div[@class="rela-journals"]/div[@class="result"]'
                articles = driver.find_elements_by_xpath(articles_xpath)
                for k in range(len(articles)):
                    try:
                        article_name_xpath = articles_xpath + '[' + str(k+1) + ']' + '/div[@class="left"]/h3/a'
                        article_name = driver.find_element_by_xpath(article_name_xpath).text
                        article_xpath = articles_xpath + '[' + str(k+1) + ']' + '/div[@class="cooper"]/a[2]/i'
                        driver.find_element_by_xpath(article_xpath).click()
                        sleep(2)
                        article_link_xpath = '//div[@class="src_download_wr"]/div[@class="src_content"]/ul/li/a[text()="知网"]'
                        # get the article link
                        article_link = driver.find_element_by_xpath(article_link_xpath).get_attribute("href")
                        print(article_name + '：' + article_link)
                        article_links.append(article_link)
                        driver.find_element_by_xpath('//div[@class="src_download_wr"]/a[@class="c-icon-close-hover close-icon dialog-close"]/i').click()
                        sleep(2)
                    except:
                        sleep(2)
                        continue
                # click next page
                try:
                    driver.find_element_by_xpath('//i[@class="c-icon c-icon-page-next"]').click()
                    sleep(2)
                    continue
                except:
                    break
            driver.delete_all_cookies()
            sleep(15)


article_links = list(set(article_links))
with open('./tszlgz_2003_2001.txt', 'w', encoding='utf-8') as f:
    for article_link in article_links:
        f.write(article_link)
        f.write('\n')
f.close()

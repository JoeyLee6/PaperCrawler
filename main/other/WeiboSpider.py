"""
微博评论爬虫
m.weibo.cn
"""
from selenium import webdriver
from time import sleep
import csv


urls = [
    'https://m.weibo.cn/status/4124833140528087',
    'https://m.weibo.cn/status/4124815021389657'
]
driver = webdriver.Firefox()

# login to Weibo
login_url = 'https://passport.weibo.cn/signin/login?entry=mweibo&res=wel&wm=3349&r=http%3A%2F%2Fm.weibo.cn%2F'
driver.get(login_url)
sleep(1)
driver.find_element_by_xpath('//input[@id="loginName"]').send_keys('')
driver.find_element_by_xpath('//input[@id="loginPassword"]').send_keys('')
driver.find_element_by_id('loginAction').click()

# iterate the urls
for url in urls:
    # create csv file
    writer = csv.writer(open(url.split('/')[-1]+'.csv', mode='w', encoding='utf-8', newline=''))
    writer.writerow(['Number', 'Username', 'Time', 'Content'])

    # get the top comments first
    driver.get(url)
    sleep(2)
    count = 0
    comments = driver.find_elements_by_xpath('//div[@class="comment-item"]')
    print('Number of Comments:', len(comments))
    for comment in comments:
        count += 1
        print('Number:', count)
        username = comment.find_element_by_class_name('comment-user-name').text
        print('Username:', username)
        time = comment.find_element_by_class_name('comment-time').text
        print('Time:', time)
        content = comment.find_element_by_class_name('comment-con').text
        print('Content:', content)
        data = [count, username, time, content]
        writer.writerow(data)
        print()
    print()

    # roll the page to get other comments
    top_index = 0
    roll_height = 10000000000
    while True:
        top_index_previous = top_index
        top_index += roll_height
        js = "var q=document.documentElement.scrollTop=" + str(top_index)
        driver.execute_script(js)
        sleep(2)
        len_comments_previous = len(comments)
        comments = driver.find_elements_by_xpath('//div[@class="comment-item"]')
        print('Number of Comments:', len(comments))
        if len_comments_previous == len(comments):
            print('THE END! EXIT CRAWLING!')
            break
        else:
            for comment in comments[count:]:
                count += 1
                print('Number:', count)
                username = comment.find_element_by_class_name('comment-user-name').text
                print('Username:', username)
                time = comment.find_element_by_class_name('comment-time').text
                print('Time:', time)
                content = comment.find_element_by_class_name('comment-con').text
                print('Content:', content)
                data = [count, username, time, content]
                writer.writerow(data)
                print()
            print()

sleep(30)
driver.close()

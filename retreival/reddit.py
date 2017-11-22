import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
import pymysql.cursors

# at the beginning:
start_time = time.time()
connection = pymysql.connect(user='root', password='abc123', host='127.0.0.1', db='trendy', cursorclass=pymysql.cursors.DictCursor)

chromeOptions = Options()
chromeOptions.add_argument("--headless")
chromeOptions.add_experimental_option('prefs', {'geolocation': True})
driver = webdriver.Chrome(chrome_options=chromeOptions)
wait = WebDriverWait(driver, 30)
driver.get("https://reddit.com/")

# Typing credentials and signing in
driver.find_element_by_name('user').send_keys('')
driver.find_element_by_name('passwd').send_keys('')
driver.find_element_by_xpath('//button[@class="btn"][@type="submit"]').click()
driver.find_element_by_xpath('//button[@class="btn"][@type="submit"]').click()
time.sleep(3)

# Parsing from Reddit
threads = []
#hrefs = []
comments = []
links = []
thread = driver.find_elements_by_xpath('//a[starts-with(@class, "title may-blank")]')
for words in thread[1:]:
    threads.append(str(words.text))
    #hrefs.append(str(words.get_attribute('href')))
commentsNum = driver.find_elements_by_xpath('//li[@class="first"]')
for comment in commentsNum:
    commentsLink = comment.find_element_by_css_selector('a').get_attribute('href')
    if not comment.text == "comment":
        comments.append(str(comment.text))
        links.append(str(commentsLink))
    else:
        comments.append("0 comments")
        links.append(str(commentsLink))

print(len(commentsNum))
try:
    username = 'alibaba'
    with connection.cursor() as cursor:
        for i in range(0, len(commentsNum)):
            # print(str(thread[i].text) + " : " + str(hrefs[i]) + " : " + str(comments[i]) + " : " + str(links[i]))
            print(str(thread[i].text) + " : " + str(comments[i]) + " : " + str(links[i]))
            sql = "INSERT INTO trendy.reddit(id, username, thread, link, loadtime) VALUES (DEFAULT, %s, %s, %s, %s, NOW())"
            cursor.execute(sql, (username, thread[i].text, comments[i], links[i]))
        connection.commit()


except:
    pass

# At the end of the program:
print("Retrieval time took %f seconds" % (time.time() - start_time))

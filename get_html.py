import sys
import string
import os
import time
import re
from bs4 import BeautifulSoup
from selenium import webdriver


# https://www.snopes.com/fact-check/page/50/
def loop_for(address, start_page):
    driver = webdriver.Chrome('./sel/chromedriver')
    main_dir = os.getcwd()

    dir_address = make_directory(main_dir)
    os.chdir(dir_address)

    for page_num in range(int(start_page),50):
        if not os.path.isfile('corona_%s.html' % (page_num)):
            with open('corona_%s.html' % (page_num), 'a') as f:
                f.write('<html>\n<head>\n<meta charset="UTF-8">\n</head><body>\n')

            page_url2 = "https://www.snopes.com/fact-check/page/%s/" % page_num
            print(page_url2)
            extract_chart(page_url2, page_num, driver)

            with open('corona_%s.html' %(page_num), 'a') as f:
                f.write('\n</body></html>\n') # append main contents
            #os.chdir(main_dir)
    


def extract_chart(page_url2, page_num, driver):
    driver.get(page_url2)
    html_source = driver.page_source
    soup = BeautifulSoup(html_source,"html.parser")
    contents = ""

    try:
        # 기사 제목 및 href, summary 포함된 정보를 html문서에서 파싱
        news_list = soup('div', attrs={'class':'media-list'})[0]
        contents = news_list.findAll("article")

    except IndexError:
        print("IndexError")

    for main_content in contents:
        with open('corona_%s.html' % (page_num), 'a') as f:
            f.write(str(main_content) + '\n<BR><BR>') # save
    

def make_directory(cur_dir):
    os.chdir(cur_dir)
    address = os.getcwd()

    if not os.path.isdir('corona_news'):
        os.mkdir('corona_news')
    address = address + '/corona_news'
    os.chdir(address)

    return address

if __name__ == "__main__":
    parent_address = os.getcwd()
    os.chdir(parent_address)
    address = os.getcwd()

try:
    start_page = sys.argv[1]

except Exception:
    print("===============")
    print("python3 crawler.py 1")

else:
    address = "https://www.snopes.com/fact-check/page/"
    loop_for(address, start_page)


"""
    for i in range(1,50):   
        page_url2 = "https://www.snopes.com/fact-check/page/%s/" % i
        driver.get(page_url2)
        print(page_url2)
        soup = BeautifulSoup(driver.page_source, "html.parser")

        d = soup.find('li',{'class':'date breadcrumb-item'}).text
        date = d.split()[0]
        month = d.split()[1]
        year = d.split()[2]
        print(month + " " + year + " " + date)
"""
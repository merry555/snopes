from urllib.request import urlopen
import sys
import string
import os
import time
import re
from bs4 import BeautifulSoup
from selenium import webdriver

def total_news(main_dir, page_html, page_num):
    with open(page_html,'r') as f:
        html = f.read()
    cur_dir = os.getcwd()
    print(cur_dir)
    os.chdir(main_dir)

    soup = BeautifulSoup(html,"html.parser")


    if not os.path.isdir("total_news"):
        os.mkdir("total_news")
    dir_address = main_dir + "/total_news"
    os.chdir(dir_address)

    with open("%s_news_body.html" % page_num, 'a') as f:
        f.write('<html>\n<head>\n<meta charset="UTF-8">\n</head><body>')

    for head in soup.findAll('a'):
        address = head.get('href')
        get_news(address, page_num)
        print(address)
        
    with open("%s_news_body.html" % page_num, 'a') as f:
        f.write('\n</body></html>')
    os.chdir(cur_dir)

def get_news(address, page_num, maxbuf=10485700):
    try:
        res = urlopen(address)
    except:
        print("url open error")
    else:
        try:
            html = res.read(maxbuf)
        except:
            os.remove("%s_news_body.html" % page_num)
            time.sleep(10)
            print("can not read html file")
        try: 
            # get body
            soup = BeautifulSoup(html,"html.parser")
            rate = soup.find('div', attrs={'class':'rating-wrapper card'})
            claim = soup.find('div', attrs={'class':'claim-wrapper card'})
            contents = soup.find('div', attrs={'class':'content-wrapper card'})
            
        except IndexError:
            print("IndexError")

        with open("%s_news_body.html" % (page_num), 'a') as f:
            f.write(str(rate) + str(claim) + str(contents)+ '\n<BR><BR>')

if __name__ == "__main__":
    parent_address = os.getcwd()
    os.chdir(parent_address)
    address = os.getcwd()

    main_dir = address + '/corona_news'
    os.chdir(main_dir)

    for i in range(1, 50):
        page_html = 'corona_%d.html' %(i)
        total_news(main_dir,page_html,i)

from urllib.request import urlopen
import sys
import string
import os
import time
import re
from bs4 import BeautifulSoup
from selenium import webdriver

# urlopen("http://www.example.com").read()

def get_title(main_dir, page_html, page_num):
    with open(page_html,'r') as f:
        html = f.read()
    cur_dir = os.getcwd()
    print(cur_dir)
    os.chdir(main_dir)

    soup = BeautifulSoup(html,"html.parser")


    if not os.path.isdir("news_body"):
        os.mkdir("news_body")
    dir_address = main_dir + "/news_body"
    os.chdir(dir_address)

    with open("%s_body.html" % page_num, 'a') as f:
        f.write('<html>\n<head>\n<meta charset="UTF-8">\n</head><body>')

    for head in soup.findAll('a'):
        address = head.get('href')
        get_body(address, page_num)
        print(address)
        
    with open("%s_body.html" % page_num, 'a') as f:
        f.write('\n</body></html>')
    os.chdir(cur_dir)
 
def get_body(address, page_num, maxbuf=10485700):
    try:
        res = urlopen(address)
    except:
        print("url open error")
    else:
        try:
            html = res.read(maxbuf)
        except:
            os.remove("%s_body.html" % page_num)
            time.sleep(10)
            print("can not read html file")
        try:
            # get body
            soup = BeautifulSoup(html,"html.parser")
            rate = soup.find('div', attrs={'class':'rating-wrapper card'})
        except IndexError:
            print("IndexError")

        with open("%s_body.html" % (page_num), 'a') as f:
            f.write(str(rate) + '\n<BR><BR>')



if __name__ == "__main__":
    parent_address = os.getcwd()
    os.chdir(parent_address)
    address = os.getcwd()

    main_dir = address + '/corona_news'
    os.chdir(main_dir)

    for i in range(1, 50):
        page_html = 'corona_%d.html' %(i)
        get_title(main_dir,page_html,i)




    
import sys
import string
import os
import time
import re
from bs4 import BeautifulSoup
import pandas as pd

def get_body(path, html,i):
    infoPrint = []  
    os.chdir(path)
    with open(html) as file:
        html = file.read()
        soup = BeautifulSoup(html,"html.parser")
        for ad in soup.findAll('div', attrs={'class':'card-body p-0'}):
            ad.extract()
        
        for contents in soup.findAll('div',attrs={'class': 'content'}):
            infolist = []
            for txt in contents.findAll('p'):
                info = txt.get_text().strip().replace('\n','')
                infolist.append(info)
            a = '\n'.join(infolist)
            infoPrint.append(str(a))

        os.chdir('/Users/jisu/corona/csv')
        result = pd.DataFrame({'body':infoPrint})
        result.to_csv("snoup_news_body_%s.csv"%(i),mode='w')

def get_source(path, html,num):
    os.chdir(path)
    printcitlist = []
    taglist = []

    with open(html) as file:
        html = file.read()
        soup = BeautifulSoup(html,"html.parser")
        # <div class="citations">

        tag = list(soup.findAll('footer'))

        for i in range(len(tag)):
            if tag[i].findAll('div',attrs={'class':'citations'}):
                citlist = []
                for s in tag[i].findAll('p'):
                    d = s.text.replace('\xa0','').replace('  ','').replace('\n','')
                    citlist.append(d)
                printcitlist.append('!$!$'.join(citlist))
            else:
                printcitlist.append('')

            # <li class="tag">

            if tag[i].findAll('li',attrs={'class':'tag'}):
                for s in tag[i].findAll('li',attrs={'class':'tag'}):
                    d = s.a.get_text()
                taglist.append(d)
            else:
                taglist.append('')

        os.chdir('/Users/jisu/corona/csv')
        

        result_source = pd.DataFrame({'source':printcitlist, 'tag':taglist})
        result_source.to_csv("snoup_news_source_%s.csv"%(num),mode='w')

if __name__ == "__main__":
    path = '/Users/jisu/corona/corona_news/news_body'

    for i in range(1,50):
        html = '%s_news_body.html' %(i)
        print(html)
        num = i
        get_source(path, html,num)
        #get_body(path, html,i)
        